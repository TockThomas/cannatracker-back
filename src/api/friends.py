from typing import List, Annotated

from fastapi import Depends, APIRouter

from src.core.controller.friend import FriendController
from src.core.models import PublicUser, UserInDB
from src.core.redis_io import Redis, redis_connection
from src.core.security import get_current_active_user

router = APIRouter()


@router.get("/friends", tags=["Friends"], response_model=List[PublicUser])
async def get_friends(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    db: Redis = Depends(redis_connection),
) -> List[PublicUser]:
    return await FriendController.get_friends(db, current_user)


@router.post("/friends/{friends_username}", tags=["Friends"])
async def add_friend(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
    friends_username: str,
    db: Redis = Depends(redis_connection),
) -> PublicUser:
    return await FriendController.add_friend(db, current_user, friends_username)


@router.delete("/friends/{friends_username}", tags=["Friends"])
async def delete_friend(
        current_user: Annotated[UserInDB, Depends(get_current_active_user)],
        friends_username: str,
        db: Redis = Depends(redis_connection),
) -> bool:  # TODO: add message
    return await FriendController.delete_friend(db, current_user, friends_username)