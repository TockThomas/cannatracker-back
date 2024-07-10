import json
import logging
import time
import traceback
from datetime import datetime, timezone
from json import JSONDecodeError
from typing import Any, Optional

import redis.asyncio as redis

from src.core.models import UserInDB


redis_connection_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)


def redis_connection() -> redis.Redis:
    return Redis(connection_pool=redis_connection_pool)


class Redis:
    REDIS_MODULE_CONFIG = "config"
    USERS = "users"
    def __init__(self, **kwargs: Any):
        self.logger = logging.getLogger(Redis.__name__)
        self.redis = redis.Redis(**kwargs)

    def __getattr__(self, attr):
        return getattr(self.redis, attr)

    async def wait_redis(self) -> None:
        while (True):  # since redis is essential to the operation of this application, lets block until it is online
            try:
                self.ping()
                self.logger.info(
                    f"Connected to redis://{self.connection_pool.connection_kwargs['host']}:{self.connection_pool.connection_kwargs['host']}. Moving forward"
                )
                break
            except ConnectionError:
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

    async def set_user(self, user: UserInDB) -> None:
        await self.hset(self.USERS, user.id, user.model_dump_json())

    """
    async def get_something(self) -> dict:
        key = "some_key"
        raw = await self.get(key)
        return self._try_json(raw)
        
    async def get_all(self) -> dict:
        key = "some_key"
        raw = await self.getall(key)
        return {key: self._try_json(value) for key, value in raw_values.items()}"""

    async def push_error(
        self, subject: str, message: str, details: Optional[BaseException]
    ) -> None:
        report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "subject": subject,
            "message": message,
        }

        if details:
            report["details"] = "".join(
                traceback.format_exception(details, limit=3, chain=False)
            )
        await self.sadd("error:reports", json.dumps(report))
