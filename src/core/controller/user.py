import uuid
from datetime import timezone, datetime
from typing import Any

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.core.models import CreateUser, User, UserInDB
from src.core.redis_io import Redis
from src.core.security import get_password_hash, get_access_token


class UserController:
    @classmethod
    async def _has_duplicate_user(
        cls, db: Redis, username: str, email: str
    ) -> bool:  # TODO: change return from bool to error message
        all_users = await db.get_all_users()
        for user in all_users.values():
            if user.get("email", "") == email:
                # TODO: make error response (DuplicateEmail)
                return True
            elif user.get("username", "") == username:
                # TODO: make error response (DuplicateUsername)
                return True
        return False

    @classmethod
    async def create_user(cls, db: Redis, form_data: CreateUser) -> User:
        if await cls._has_duplicate_user(db, form_data.username, form_data.email):
            raise HTTPException(400, "Username/Email already taken")
        user_id = str(uuid.uuid4())
        password_hashed = get_password_hash(form_data.password)
        now = datetime.now(timezone.utc)
        user_dict = {
            "id": user_id,
            "email": form_data.email,
            "first_name": form_data.first_name,
            "last_name": form_data.last_name,
            "username": form_data.username,
            "password": password_hashed,
            "plants": [],
            "collaborated_plants": [],
            "schedule_templates": [],
            "created_at": now,
            "updated_at": now,
            "disabled": False,
        }
        user_db = UserInDB.model_validate(user_dict)
        await db.set_user(user_db)
        user = user_db.to_user_model()
        return user

    @classmethod
    async def login(cls, db: Redis, form_data: OAuth2PasswordRequestForm):
        users = await db.get_all_users()
        token = await get_access_token(users, form_data)
        return token
