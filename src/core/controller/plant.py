import uuid
from datetime import datetime, timezone
from typing import List

from src.core.models import CreatePlant, Plant, User, UserInDB, PlantInDB
from src.core.redis_io import Redis


class PlantController:
    @classmethod
    async def create_plant(cls, db: Redis, current_user, data: CreatePlant) -> Plant:
        plant_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        plant_dict = {
            "id": plant_id,
            "name": data.name,
            "owner": current_user.id,
            "set_watering_period": data.set_watering_period,
            "set_watering_amount": data.set_watering_amount,
            "collaboration": data.collaboration,
            "schedules": data.schedules,
            "watering_records": [],
            "start_date": data.start_date,
            "end_date": now,
            "created_at": now,
            "updated_at": now,
            "active": True
        }
        try:
            plant = PlantInDB.model_validate(plant_dict)
            await db.set_plant(plant)
            return plant
        except Exception as e:
            print(e)

    @classmethod
    async def get_plants(cls, db: Redis, current_user: User) -> List[Plant]:
        plant_ids = current_user.plants
        plants = await db.get_plants(plant_ids)
        return plants

    @classmethod
    async def get_plant(cls, db: Redis, current_user: User, plant_id: str) -> Plant:
        plant = await db.get_plant(plant_id)
        return plant

    @classmethod
    async def update_plant(cls, db: Redis, current_user: User, data: Plant) -> Plant:
        plant = data
        plant.updated_at = datetime.now(timezone.utc)
        await db.set_plant(plant)
        return plant

    @classmethod
    async def delete_plant(cls, db: Redis, current_user: User, plant_id: str) -> None:  # TODO: Change to SuccessNotification
        if not plant_id in current_user.plants:
            return
        await db.delete_plant(plant_id)
        # remove plant_id from User
        model = await db.get_user(current_user.id)
        user_in_db = UserInDB.model_validate(model)
        user_in_db.updated_at = datetime.now(timezone.utc)
        user_in_db.plants.remove(plant_id)
        await db.set_user(user_in_db)

