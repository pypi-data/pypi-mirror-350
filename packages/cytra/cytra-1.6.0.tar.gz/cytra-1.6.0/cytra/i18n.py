import logging
from os.path import exists

from babel.support import Translations

from cytra import get_current_app
from cytra.helpers import LazyString

logger = logging.getLogger("cytra")


def get_request_locales(headers):
    # e.g. 'es,en-US;q=0.8,en;q=0.6'
    locale_header = headers.get("accept-language", "").strip()
    if not locale_header:
        return

    if ";q=" in locale_header:
        # Extract all locales and their preference (q)
        locales = set()  # e.g. [('es', 1.0), ('en-US', 0.8), ('en', 0.6)]
        for locale_str in locale_header.split(","):
            locale_parts = locale_str.split(";q=")
            locales.add(
                (
                    locale_parts[0],
                    float(locale_parts[1]) if len(locale_parts) > 1 else 1.0,
                )
            )
        locales = map(
            lambda x: x[0],
            sorted(locales, key=lambda x: x[1], reverse=True),
        )
    else:
        locales = locale_header.split(",")

    # Sort locales according to preference
    for locale in locales:
        parts = locale.strip().split("-")
        if len(parts) == 1:
            yield parts[0], None
        else:
            yield parts[0], parts[1].upper()


def _translate(*args, **kwargs):
    app = get_current_app()
    assert app, "No application configured"
    assert hasattr(app, "locales"), "The i18n extension not configured"
    assert app.locales, "No i18n locales configured"

    return app._translate(*args, **kwargs)


def translate(*args, **kwargs):
    return LazyString(_translate, *args, **kwargs)


class I18nAppMixin:
    """
    Internationalization Mixin

    Configuration:

    Example configuration in YAML:
        i18n:
          locales:
            - en_US
            - fa_IR
          localedir: myapp/i18n
          domain: app

    Note: First locale will set as default.

    Change locale:
        >>> app.locale = 'en_US'

    Translate:
        >>> app.translate('HelloWorld')
        or
        >>> cytra.translate('HelloWorld')
    """

    locales = None
    translate = translate

    def setup(self):
        super().setup()

        # i18n not configured
        if "i18n" not in self.config:  # pragma: nocover
            return

        # no locales defined
        i18n_conf = dict(self.config.i18n)
        locales = i18n_conf.get("locales")

        if not locales:
            self.log.info(
                "The i18n extension configured but not `locales` defined"
            )
            return

        localedir = i18n_conf.get("localedir")
        if not exists(localedir):
            raise FileNotFoundError(
                f"Locales directory not found '{localedir}'"
            )

        # e.g., ['en_US', 'fr_FR']
        self.locales = tuple(locales)

        # e.g., [('en', 'US'), ('fr', 'FR')]
        self.locales_tuple = tuple(map(lambda x: tuple(x.split("_")), locales))
        self.translations = {}

        # Load translations using Babel
        for locale in locales:
            self.translations[locale] = Translations.load(
                dirname=localedir,
                locales=[locale],
                domain=i18n_conf.get("domain"),
            )

    def on_begin_request(self):
        super().on_begin_request()
        self.locale = None
        self.set_locale_from_request()

    def on_end_response(self):
        super().on_end_response()
        self.locale = None

    @property
    def locale(self):
        if not self.locales:
            return

        if not self.request:
            return self.locales[0]

        return self.request._locale

    @locale.setter
    def locale(self, v):
        if v is not None:
            self.validate_locale(v)
            self.response.headers["content-language"] = v.replace("-", "_")
        self.request._locale = v

    def _find_locale_from_request(self):
        # get_request_locales extracts (language, region) tuples from headers
        request_locales = tuple(get_request_locales(self.request.headers))
        if not request_locales:
            return

        # Find exact match
        for locale in request_locales:
            for locale_ in self.locales_tuple:
                if locale == locale_:
                    return locale_

        # Find by language match
        for lang, region in request_locales:
            for lang_, region_ in self.locales_tuple:
                if lang == lang_:
                    return lang_, region_

    def set_locale_from_request(self):
        locale_tuple = self._find_locale_from_request()
        if locale_tuple:
            self.locale = "_".join(locale_tuple)
        else:
            # Set default locale
            self.locale = self.locales[0]

    def validate_locale(self, locale):
        if locale not in self.locales:
            raise ValueError(f"Locale not defined `{locale}`")

        return locale

    def _translate(self, word, plural=None, n=None):
        translation = self.translations.get(self.locale)
        if plural is not None:
            return translation.ngettext(word, plural, n)
        return translation.gettext(word)
