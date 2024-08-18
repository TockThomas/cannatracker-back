from typing import Annotated, List

from fastapi import APIRouter, Depends

from src.core.controller.schedule_template import ScheduleTemplateController
from src.core.models import User, ScheduleTemplate, CreateScheduleTemplate
from src.core.redis_io import redis_connection, Redis
from src.core.security import get_current_active_user

router = APIRouter()


@router.get("/templates", tags=["ScheduleTemplate"])
async def get_templates(
        current_user: Annotated[User, Depends(get_current_active_user)],
        db: Redis = Depends(redis_connection)
) -> List[ScheduleTemplate]:
    return await ScheduleTemplate.get_templates(db, current_user)


@router.get("/templates/{template_id}", tags=["ScheduleTemplate"])
async def get_template(
        current_user: Annotated[User, Depends(get_current_active_user)],
        template_id: str,
        db: Redis = Depends(redis_connection)
) -> ScheduleTemplate:
    return await ScheduleTemplateController.get_template(db, current_user, template_id)


@router.put("/templates/{template_id}", tags=["ScheduleTemplate"])
async def update_template(
        current_user: Annotated[User, Depends(get_current_active_user)],
        form_data: ScheduleTemplate,
        db: Redis = Depends(redis_connection)
) -> ScheduleTemplate:
    return await ScheduleTemplateController.update_template(db, current_user, form_data)


@router.post("/templates", tags=["ScheduleTemplate"])
async def create_template(
        current_user: Annotated[User, Depends(get_current_active_user)],
        form_data: CreateScheduleTemplate,
        db: Redis = Depends(redis_connection)
) -> ScheduleTemplate:
    return await ScheduleTemplateController.create_template(db, current_user, form_data)


@router.delete("/templates/{template_id}", tags=["ScheduleTemplate"])
async def delete_template(
        current_user: Annotated[User, Depends(get_current_active_user)],
        template_id: str,
        db: Redis = Depends(redis_connection)
) -> None:  # TODO: add message
    return await ScheduleTemplateController.delete_template(db, current_user, template_id)
