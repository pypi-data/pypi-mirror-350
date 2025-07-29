from redis import Redis


class RedisAppMixin:
    redis = None

    def setup(self):
        if "redis" in self.config:
            self.redis = Redis(**dict(self.config.redis))
        else:
            self.redis = None
        super().setup()

    def shutdown(self):
        super().shutdown()
        if "redis" in self.config:
            self.redis.close()
