from typing import List, Annotated

from fastapi import Depends, APIRouter

from src.core.controller.plant import PlantController
from src.core.models import CreatePlant, Plant, UserInDB
from src.core.redis_io import Redis, redis_connection
from src.core.security import get_current_active_user

router = APIRouter()


@router.get("/plants", tags=["Plants"], response_model=List[Plant])
async def get_plants(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db: Redis = Depends(redis_connection),
) -> List[Plant]:
    return await PlantController.get_plants(db, current_user)


@router.get("/plants/{plant_id}", tags=["Plants"])
async def get_plant(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    plant_id: str,
    db: Redis = Depends(redis_connection),
) -> Plant:
    return await PlantController.get_plant(db, current_user, plant_id)


@router.put("/plants/{plant_id}", tags=["Plants"])
async def update_plant(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    form_data: Plant,
    db: Redis = Depends(redis_connection),
) -> Plant:
    return await PlantController.update_plant(db, current_user, form_data)


@router.post("/plants", tags=["Plants"])
async def create_plant(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    form_data: CreatePlant,
    db: Redis = Depends(redis_connection),
) -> Plant:
    return await PlantController.create_plant(db, current_user, form_data)


@router.delete("/plants/{plant_id}", tags=["Plants"])
async def delete_plant(
        current_user: Annotated[UserInDB, Depends(get_current_active_user)],
        plant_id: str,
        db: Redis = Depends(redis_connection),
) -> None:  # TODO: add message
    return await PlantController.delete_plant(db, current_user, plant_id)