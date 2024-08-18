from datetime import timezone, datetime
from typing import List

from src.core.models import ScheduleTemplate, User, UserInDB, CreateScheduleTemplate
from src.core.redis_io import Redis


class ScheduleTemplateController:
    @classmethod
    async def create_template(cls, db: Redis, current_user: User, template: CreateScheduleTemplate):
        pass
        # TODO: create template

    @classmethod
    async def get_templates(cls, db: Redis, current_user: User) -> List[ScheduleTemplate]:
        public_template_ids = []
        # TODO: read config from redis
        custom_template_ids = current_user.schedule_templates
        template_ids = public_template_ids + custom_template_ids
        templates = await db.get_templates(template_ids)
        return templates

    @classmethod
    async def get_template(cls, db: Redis, current_user: User, template_id: str) -> ScheduleTemplate:
        template = await db.get_template(template_id)
        return template

    @classmethod
    async def update_template(cls, db: Redis, current_user: User, data: ScheduleTemplate) -> ScheduleTemplate:
        template = data
        template.updated_at = datetime.now(timezone.utc)
        await db.set_template(template)
        return template

    @classmethod
    async def delete_template(cls, db: Redis, current_user: User, template_id: str) -> None:  # TODO: change
        if not template_id in current_user.schedule_templates:
            return
        await db.delete_template(template_id)
        # remove template_id from User
        model = await db.get_user(current_user.id)
        user_in_db = UserInDB.model_validate(model)
        user_in_db.updated_at = datetime.now(timezone.utc)
        user_in_db.schedule_templates.remove(template_id)
        await db.set_user(user_in_db)


