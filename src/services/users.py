from src.schemas.users import User
from src.services.base import BaseService


class UserService(BaseService):
    async def get_user(self, user_id: int) -> User:
        return await self.db.users.get_one_or_none(id=user_id)
