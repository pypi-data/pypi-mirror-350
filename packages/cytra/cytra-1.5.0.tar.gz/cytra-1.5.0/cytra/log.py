from logging import getLogger, shutdown
from logging.config import dictConfig


class LogAppMixin:
    _logger_name = "main"

    def setup(self):
        if "logging" in self.config:
            dictConfig(dict(self.config.logging))
            self.log = getLogger(self._logger_name)
        super().setup()

    def shutdown(self):
        super().shutdown()
        if "logging" in self.config:
            shutdown()
            del self.log
