from typing import List

from src.core.models import UserInDB, PublicUser
from src.core.redis_io import Redis


class FriendController:
    @classmethod
    async def add_friend(cls, db: Redis, current_user: UserInDB, friends_username: str) -> PublicUser:
        if friends_username == current_user.username:
            raise Exception('You cannot add a friend yourself!')
        all_users = await db.get_all_users()
        for user in all_users:
            if user.username == friends_username:
                friend = user
                current_user.friends.append(friend.id)
                ### accept automaticly friendrequest
                friend.friends.append(current_user.id)
                ### save in db
                await db.set_user(current_user)
                await db.set_user(friend)
                return await db.get_public_user(friend.id)
        raise Exception('Friends not found')


    @classmethod
    async def get_friends(cls, db: Redis, current_user: UserInDB) -> List[PublicUser]:
        friends = current_user.friends
        public_users = []
        for friend in friends:
            public_user = await db.get_public_user(friend)
            public_users.append(public_user)
        return public_users

    @classmethod
    async def delete_friend(cls, db: Redis, current_user: UserInDB, friends_username: str) -> bool:  # TODO: Change to SuccessNotification
        all_users = await db.get_all_users()
        friend = None
        for user in all_users:
            if user.username == friends_username:
                friend = user
                break
        if not friend or friend.id not in current_user.friends:
            raise Exception('Friends not found')
        current_user.friends.remove(friend.id)
        ### delete user from friend
        friend.friends.remove(current_user.id)
        ### save in db
        await db.set_user(current_user)
        await db.set_user(friend)
        return True
