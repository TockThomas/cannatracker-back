import uuid
from datetime import datetime, timezone, date
from typing import List

from src.core.models import CreatePlant, Plant, UserInDB, PlantInDB, WateringRecord
from src.core.redis_io import Redis


class PlantController:
    @classmethod
    async def create_plant(cls, db: Redis, current_user: UserInDB, data: CreatePlant) -> Plant:
        plant_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        schedules = await db.get_template(data.schedules)
        start_date = datetime.strptime(data.start_date, "%Y-%m-%d").date()
        collaborators = await cls.convert_username_to_id(db, data.collaborators)
        plant_dict = {
            "id": plant_id,
            "name": data.name,
            "owner": current_user.id,
            "set_watering_period": data.set_watering_period,
            "set_watering_amount": data.set_watering_amount,
            "collaborators": collaborators,
            "schedule": schedules,
            "watering_records": [],
            "start_date": start_date,
            "end_date": now.date(),
            "created_at": now,
            "updated_at": now,
            "active": True
        }
        try:
            plant_in_db = PlantInDB.model_validate(plant_dict)
            await db.set_plant(plant_in_db)
            # add plant to users
            current_user.plants.append(plant_in_db.id)
            await db.set_user(current_user)
            for collaborator in plant_in_db.collaborators:
                model = await db.get_user(collaborator)
                user_in_db = UserInDB.model_validate(model)
                user_in_db.collaborated_plants.append(plant_in_db.id)
                await db.set_user(user_in_db)
            plant = await db.get_plant(plant_in_db.id)
            return plant
        except Exception as e:
            print(e)

    @classmethod
    async def get_plants(cls, db: Redis, current_user: UserInDB) -> List[Plant]:
        plant_ids = current_user.plants + current_user.collaborated_plants
        plants = await db.get_plants(plant_ids)
        return plants

    @classmethod
    async def get_plant(cls, db: Redis, current_user: UserInDB, plant_id: str) -> Plant:
        plant = await db.get_plant(plant_id)
        return plant

    @classmethod
    async def update_plant(cls, db: Redis, current_user: UserInDB, data: Plant) -> Plant:
        plant = data
        plant.updated_at = datetime.now(timezone.utc)
        await db.set_plant(plant)
        return plant

    @classmethod
    async def delete_plant(cls, db: Redis, current_user: UserInDB, plant_id: str) -> None:  # TODO: Change to SuccessNotification
        if not plant_id in current_user.plants:
            return
        await db.delete_plant(plant_id)
        # remove plant_id from User
        model = await db.get_user(current_user.id)
        user_in_db = UserInDB.model_validate(model)
        user_in_db.updated_at = datetime.now(timezone.utc)
        user_in_db.plants.remove(plant_id)
        await db.set_user(user_in_db)

    @classmethod
    async def water_plant(cls, db: Redis, current_user: UserInDB, plant_id: str) -> bool:
        if not plant_id in current_user.plants + current_user.collaborated_plants:
            return False
        plant = await db.get_plant(plant_id)
        model = {
            "actor": current_user.username,
            "created_at": datetime.now(timezone.utc)
        }
        watering_record = WateringRecord.model_validate(model)
        plant.watering_records.append(watering_record)
        await db.set_plant(plant)
        return True

    @staticmethod
    async def convert_username_to_id(db: Redis, usernames: List[str]) -> List[str]:
        if not usernames:
            return []
        ids = []
        all_users = await db.get_all_users()
        for username in usernames:
            for user in all_users:
                if user.username == username:
                    ids.append(user.id)
        return ids
