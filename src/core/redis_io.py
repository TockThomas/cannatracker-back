import json
import logging
import time
import traceback
from datetime import datetime, timezone
from json import JSONDecodeError
from typing import Any, Optional, List

import redis.asyncio as redis

from src.core.controller import user
from src.core.models import UserInDB, Plant, PlantInDB, ScheduleTemplate, AbstractPlant

redis_connection_pool = redis.ConnectionPool(host="localhost", port=6379, db=0)


def redis_connection() -> redis.Redis:
    return Redis(connection_pool=redis_connection_pool)


class Redis:
    REDIS_MODULE_CONFIG = "config"
    USERS = "users"
    PLANTS = "plants"
    TEMPLATES = "templates"

    def __init__(self, **kwargs: Any):
        self.logger = logging.getLogger(Redis.__name__)
        self.redis = redis.Redis(**kwargs)

    def __getattr__(self, attr):
        return getattr(self.redis, attr)

    async def wait_redis(self) -> None:
        while (
            True
        ):  # since redis is essential to the operation of this application, lets block until it is online
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

    def _plant_load_users(self, model: dict) -> dict:
        """change collaborator list or owner from ids to User objs"""
        # owner
        owner_id = model.get("owner", {}).get("id")
        model.update({"owner": owner_id})
        # collaborators
        collaborator_ids = model.get("collaborators", [])
        collaborators_users = []
        for collaborator_id in collaborator_ids:
            collaborators_users.append(self.get_user(collaborator_id))
        model.update({"collaborators": collaborators_users})
        return model

    async def get_config(self) -> dict:
        raw = await self.get(self.REDIS_MODULE_CONFIG)
        return self._try_json(raw)

    async def get_all_users(self) -> dict:
        raw = await self.hgetall(self.USERS)
        return {key: self._try_json(value) for key, value in raw.items()}

    async def get_user(self, user_id: str) -> dict:
        raw = await self.hget(self.USERS, user_id)
        return self._try_json(raw)

    async def set_user(self, user: UserInDB) -> None:
        await self.hset(self.USERS, user.id, user.model_dump_json())

    async def get_plants(self, plant_ids: List[str]) -> List[Plant]:
        plants = []
        for plant_id in plant_ids:
            raw = await self.hget(self.PLANTS, plant_id)
            plant = self._try_json(raw)
            plant = self._plant_load_users(plant)
            plants.append(Plant.model_validate(plant))
        return plants

    async def get_plant(self, plant_id: str) -> Plant:
        raw = await self.hget(self.PLANTS, plant_id)
        model = self._try_json(raw)
        model = self._plant_load_users(model)
        return Plant.model_validate(model)

    async def set_plant(self, plant: AbstractPlant) -> None:
        if isinstance(plant, Plant):
            plant_in_db = plant.to_db_model()
        else:
            plant_in_db = plant  # If not Plant, then already PlantInDB
        model = plant_in_db.model_dump_json()
        await self.hset(self.PLANTS, plant_in_db.id, model)

    async def delete_plant(self, plant_id: str) -> None:
        await self.hdel(self.PLANTS, plant_id)

    async def get_templates(self, template_ids: List[str]) -> List[ScheduleTemplate]:
        templates = []
        for template_id in template_ids:
            raw = await self.hget(self.TEMPLATES, template_id)
            template = self._try_json(raw)
            templates.append(ScheduleTemplate.model_validate(template))
        return templates

    async def get_template(self, template_id: str) -> ScheduleTemplate:
        raw = await self.hget(self.TEMPLATES, template_id)
        model = self._try_json(raw)
        return ScheduleTemplate.model_validate(model)

    async def set_template(self, template: ScheduleTemplate) -> None:
        model = template.to_db_model()
        await self.hset(self.TEMPLATES, template.id, model)

    async def delete_template(self, template_id: str) -> None:
        await self.hdel(self.TEMPLATES, template_id)

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
