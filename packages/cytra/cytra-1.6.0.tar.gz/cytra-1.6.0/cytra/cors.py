from typing import Union

from gongish import HTTPNoContent


class CORS:
    """
    Cross-Origin Resource Sharing (CORS) is an HTTP-header based mechanism
    that allows a server to indicate any origins (domain, scheme, or port)
    other than its own from which a browser should permit loading of resources.
    CORS also relies on a mechanism by which browsers make a "preflight"
    request to the server hosting the cross-origin resource, in order to check
    that the server will permit the actual request. In that preflight,
    the browser sends headers that indicate the HTTP method and headers that
    will be used in the actual request.
    https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS

    """

    allow_origin: Union[None, str] = None
    """
    The Access-Control-Allow-Origin response header indicates whether
    the response can be shared with requesting code from the given origin.

    Directives:
    *: For requests without credentials, the literal value "*" can
        be specified, as a wildcard; the value tells browsers to allow
        requesting code from any origin to access the resource.
        Attempting to use the wildcard with credentials will result
        in an error.
    <origin>: Specifies an origin. Only a single origin can be specified.
        If the server supports clients from multiple origins, it must return
        the origin for the specific client making the request.
    """

    allow_methods: Union[None, set, str] = None
    """
    The Access-Control-Allow-Methods response header specifies the method or
    methods allowed when accessing the resource in response to a preflight
    request.

    Directives:
    set: list of the allowed HTTP request methods.
    *: The value "*" only counts as a special wildcard value for requests
        without credentials (requests without HTTP cookies or
        HTTP authentication information).
        In requests with credentials, it is treated as the literal method name
        "*" without special semantics.
    """

    allow_headers: Union[None, set, str] = None
    """
    The Access-Control-Allow-Headers response header is used in response to
    a preflight request which includes the Access-Control-Request-Headers to
    indicate which HTTP headers can be used during the actual request.

    Directives:
    set: list of the allowed HTTP request headers.
    *: The value "*" only counts as a special wildcard value for requests
        without credentials (requests without HTTP cookies or
        HTTP authentication information). In requests with credentials,
        it is treated as the literal header name "*" without special semantics.
        Note that the Authorization header can't be wildcarded and always needs
        to be listed explicitly.
    """

    expose_headers: Union[None, set, str] = None
    """
    The Access-Control-Expose-Headers response header allows a server to
    indicate which response headers should be made available to scripts running
    in the browser, in response to a cross-origin request.

    Directives:
    set: A list of header names that clients are allowed to access from a
        response.
        These are in addition to the CORS-safelisted response headers.

    *: The value "*" only counts as a special wildcard value for
        requests without credentials (requests without HTTP cookies or
        HTTP authentication information).
        In requests with credentials, it is treated as the literal header
        name "*" without special semantics. Note that the Authorization header
        can't be wildcarded and always needs to be listed explicitly.
    """

    allow_credentials: Union[None, bool] = None
    """
    Indicates whether or not the response to the request can be exposed when
    the credentials flag is true.
    """

    max_age: Union[None, int] = None
    """
    The Access-Control-Max-Age response header indicates how long the results
    of a preflight request (that is the information contained in the
    Access-Control-Allow-Methods and Access-Control-Allow-Headers headers) can
    be cached.

    Directives:
    Maximum number of seconds the results can be cached.
    Firefox caps this at 24 hours (86400 seconds).
    Chromium (prior to v76) caps at 10 minutes (600 seconds).
    Chromium (starting in v76) caps at 2 hours (7200 seconds).
    Chromium also specifies a default value of 5 seconds.
    A value of -1 will disable caching, requiring a preflight OPTIONS check
    for all calls.
    """

    def __init__(self) -> None:
        self.allow_origin = None
        self.allow_methods = set()
        self.allow_headers = set()
        self.allow_credentials = None
        self.expose_headers = set()
        self.max_age = None

    @property
    def headers(self):
        res = dict()
        if self.allow_origin is not None:
            res["access-control-allow-origin"] = self.allow_origin

        if self.allow_methods is not None:
            res["access-control-allow-methods"] = (
                ",".join(self.allow_methods).upper()
                if isinstance(self.allow_methods, set)
                else self.allow_methods
            )

        if self.allow_headers is not None:
            res["access-control-allow-headers"] = (
                ",".join(self.allow_headers)
                if isinstance(self.allow_headers, set)
                else self.allow_headers
            )

        if self.allow_credentials is True:
            res["access-control-allow-credentials"] = "true"

        if self.expose_headers is not None:
            res["access-control-expose-headers"] = (
                ",".join(self.expose_headers)
                if isinstance(self.expose_headers, set)
                else self.expose_headers
            )

        return res


class CORSAppMixin:
    def _set_cors(self):
        self.response.headers.update(self._cors_headers)

    def dispatch(self, path, verb):
        if verb == "options":

            def handler():
                raise HTTPNoContent

            return handler, ()

        return super().dispatch(path, verb)

    def on_begin_response(self):
        self._set_cors()
        return super().on_begin_response()

    def on_error(self, exc):
        self._set_cors()
        return super().on_error(exc)

    def setup(self):
        super().setup()
        self.cors.allow_methods.update(self.verbs)
        self._cors_headers = self.cors.headers
        self.verbs.add("options")

    def shutdown(self):
        super().shutdown()
        self._cors_headers = None
        self.verbs.remove("options")
