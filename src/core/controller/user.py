import uuid
from datetime import timezone, datetime
from typing import Any

from fastapi.security import OAuth2PasswordRequestForm

from src.core.models import CreateUser, User, UserInDB
from src.core.redis_io import Redis


class UserController:
    @staticmethod
    async def create_user(db: Redis, form_data: CreateUser) -> User:
        user_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        user_dict = {
            "id": user_id,
            "email": form_data.email,
            "first_name": form_data.first_name,
            "last_name": form_data.last_name,
            "username": form_data.username,
            "password": form_data.password,
            "plants": [],
            "created_at": now,
            "updated_at": now,
            "disabled": False
        }
        try:
            user_db = UserInDB.model_validate(user_dict)
            await db.set_user(user_db)
            user_dict.pop("password")
            user = User.model_validate(user_dict)
            return user
        except Exception as e:
            print(e)

