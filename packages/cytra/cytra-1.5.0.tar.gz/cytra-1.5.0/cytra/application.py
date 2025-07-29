from gongish import Application as GongishApp

from cytra.auth import AuthAppMixin
from cytra.cors import CORS
from cytra.db import DatabaseAppMixin
from cytra.log import LogAppMixin
from cytra.redis import RedisAppMixin


class CytraAppBase(GongishApp):
    # Reserved CORS config
    cors: CORS = None

    @staticmethod
    def format_json(request, response, indent=None):
        if hasattr(response.body, "to_dict"):
            response.body = response.body.to_dict()
        elif hasattr(response.body, "expose"):
            response.body = response.body.expose()
        GongishApp.format_json(request, response, indent)

    default_formatter = format_json

    def __init__(self):
        super().__init__()
        self.cors = CORS()
        self.cors.allow_headers.add("content-type")
        self.cors.expose_headers.add("content-type")

    def setup(self):
        super().setup()

    def shutdown(self):
        super().shutdown()


class Application(
    AuthAppMixin,
    RedisAppMixin,
    DatabaseAppMixin,
    LogAppMixin,
    CytraAppBase,
):
    pass
