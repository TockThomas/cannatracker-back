from fastapi import Depends, APIRouter

from src.core.controller.plant import PlantController
from src.core.models import CreatePlant, Plant
from src.core.redis_io import Redis, redis_connection


router = APIRouter()


@router.post("/plants", tags=["Plant"])
async def create_plant(form_data: CreatePlant, db: Redis = Depends(redis_connection)) -> Plant:
    return await PlantController.create_plant(db, form_data)
