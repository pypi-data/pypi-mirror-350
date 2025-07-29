from typing import Union

import jwt
from gongish import HTTPBadRequest, HTTPUnauthorized

from cytra.auth.principal import DefaultJWTPrincipal, JWTPrincipal


class Authenticator:
    header_token_key = "HTTP_AUTHORIZATION"
    jwt_principal = DefaultJWTPrincipal

    def __init__(self, app) -> None:
        self.app = app

    def create_token(self, payload: dict):
        return JWTPrincipal(app=self.app, payload=payload).dump()

    def get_principal(self) -> Union[None, JWTPrincipal]:
        try:
            return self.__class__.jwt_principal(app=self.app).load(
                self.app.request.environ[self.header_token_key]
            )

        except jwt.ExpiredSignatureError:
            raise HTTPUnauthorized("Access token expired")

        except jwt.InvalidTokenError:
            pass

    def authenticate_request(self):
        self.app.identity = None
        if self.header_token_key not in self.app.request.environ:
            return

        encoded_token = self.app.request.environ[self.header_token_key]
        if encoded_token is None or not encoded_token.strip():
            return

        self.app.identity = self.get_principal()
        if not self.app.identity:
            raise HTTPBadRequest
