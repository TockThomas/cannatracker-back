from typing import Annotated

from fastapi import Depends, APIRouter, Request
from fastapi.security import OAuth2PasswordRequestForm

from src.core.controller.user import UserController
from src.core.models import Token, User, CreateUser
from src.core.redis_io import Redis, redis_connection
from src.core.security import get_access_token


router = APIRouter()


@router.post("/login", tags=["User"])
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    return await get_access_token(form_data)


@router.post("/signup", tags=["User"])
async def create_user(form_data: Annotated[CreateUser, Depends()], db: Redis = Depends(redis_connection)) -> User:
    return await UserController.create_user(db, form_data)
