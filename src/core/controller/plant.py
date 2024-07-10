import uuid
from datetime import datetime, timezone

from src.core.models import CreatePlant, Plant
from src.core.redis_io import Redis


class PlantController:
    @staticmethod
    async def create_plant(db: Redis, data: CreatePlant) -> Plant:
        plant_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        plant_dict = {
            "id": plant_id,
            "name": data.name,
            "collaboration": data.collaboration,
            "grow_stages": data.grow_stages,
            "start_date": data.start_date,
            "end_date": now,
            "created_at": now,
            "updated_at": now,
        }
        try:
            plant = Plant.model_validate(plant_dict)
            await db.set_plant(plant)
            return plant
        except Exception as e:
            print(e)
