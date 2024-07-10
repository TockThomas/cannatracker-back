from typing import Annotated

from fastapi import Depends, APIRouter

from src.core.models import User
from src.core.security import get_user_info


router = APIRouter()


@router.get("/users/me", tags=["users"])
async def read_users_me(current_user: Annotated[User, Depends()]):
    return get_user_info(current_user)
