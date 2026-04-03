from src.schemas.roles import Role
from src.services.base import BaseService


class AdminService(BaseService):
    async def get_users(self):
        pass

    async def get_role(self, user_id: int) -> Role:
        return await self.db.roles.get_one_or_none(user_id=user_id)
