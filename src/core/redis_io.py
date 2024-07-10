import json
import logging
from datetime import time
from json import JSONDecodeError
from typing import Any

import redis


class Redis:
    REDIS_MODULE_CONFIG = "config"
    def __init__(self, **kwargs: Any):
        self.logger = logging.getLogger(Redis.__name__)
        self.redis = redis.Redis(**kwargs)

    def __getattr__(self, attr):
        return getattr(self.redis, attr)

    async def wait_redis(self) -> None:
        while (True):  # since redis is essential to the operation of this application, lets block until it is online
            try:
                await self.ping()
                self.logger.info(
                    f"Connected to redis://{self.connection_pool.connection_kwargs['host']}:{self.connection_pool.connection_kwargs['host']}. Moving forward"
                )
                break
            except ConnectionError as e:
                self.logger.error(
                    f"Connected to redis://{self.connection_pool.connection_kwargs['host']}:{self.connection_pool.connection_kwargs['host']}. Will try"
                    "again in 10 secs"
                )
                time.sleep(10)

    def _try_json(self, raw: str) -> dict or None:
        if raw is None:
            return None
        else:
            try:
                res = json.loads(raw)
            except JSONDecodeError:
                self.logger.warning(f"Can't decode {raw} to json")
                res = None
            return res

    async def get_config(self) -> dict:
        raw = await self.get(self.REDIS_MODULE_CONFIG)
        return self._try_json(raw)
