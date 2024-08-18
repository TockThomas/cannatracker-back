from typing import Annotated

from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from src.core.controller.user import UserController
from src.core.models import User, Token, CreateUser
from src.core.redis_io import Redis, redis_connection
from src.core.security import get_user_info


router = APIRouter()

@router.post("/login", tags=["User"])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Redis = Depends(redis_connection),
) -> Token:
    return await UserController.login(db, form_data)


@router.post("/signup", tags=["User"])
async def create_user(
    form_data: Annotated[CreateUser, Depends()], db: Redis = Depends(redis_connection)
) -> User:
    return await UserController.create_user(db, form_data)


@router.get("/users/me", tags=["User"])
async def read_users_me(current_user: Annotated[User, Depends()]):
    return get_user_info(current_user)
