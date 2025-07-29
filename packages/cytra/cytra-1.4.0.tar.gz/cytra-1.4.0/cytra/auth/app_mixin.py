import functools

from gongish import HTTPForbidden, HTTPUnauthorized

from cytra.auth import Authenticator


class AuthAppMixin:
    authenticator = Authenticator
    auth = None

    def on_begin_request(self):
        self.identity = None

        if self.auth:
            self.auth.authenticate_request()

        super().on_begin_request()

    def on_end_response(self):
        super().on_end_response()
        self.identity = None

    @property
    def identity(self):
        return self.request and self.request.identity

    @identity.setter
    def identity(self, value):
        self.request.identity = value

    def setup(self):
        super().setup()
        if "auth" in self.config:
            self.auth = self.__class__.authenticator(app=self)
            self.cors.allow_headers.add("authorization")
            self.cors.expose_headers.add("x-new-jwt-token")
        else:
            self.auth = None

    def shutdown(self):
        if self.auth is not None:
            self.auth = None
        super().shutdown()

    def authorize(self, *roles):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):

                if not self.identity:
                    raise HTTPUnauthorized("No identity")

                if len(roles) > 0 and not self.identity.is_in_roles(*roles):
                    raise HTTPForbidden

                return func(*args, **kwargs)

            return wrapper

        if roles and callable(roles[0]):
            f = roles[0]
            roles = []
            return decorator(f)
        else:
            return decorator
