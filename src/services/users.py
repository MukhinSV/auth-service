from src.exceptions import NoDataForUpdateException
from src.schemas.users import User, UserUpdatePartly, UserUpdate, \
    UserUpdatePartlyForAdmin
from src.services.base import BaseService


class UserService(BaseService):
    async def get_user_with_rels(self, user_id: int) -> User:
        return await self.db.users.get_one_or_none_with_rels(id=user_id)

    async def update(
            self,
            user_id: int,
            user_data: UserUpdate
    ) -> None:
        await self.db.users.update(user_data, id=user_id)
        await self.db.commit()

    async def update_partly(
            self,
            user_id: int,
            user_data: UserUpdatePartly
    ) -> None:
        if not user_data.model_dump(exclude_unset=True):
            raise NoDataForUpdateException
        await self.db.users.update(user_data, exclude_unset=True, id=user_id)
        await self.db.commit()

    async def delete_softly(self, user_id: int) -> None:
        await self.db.users.update(
            UserUpdatePartlyForAdmin(is_active=False),
            exclude_unset=True,
            id=user_id
        )
        await self.db.commit()
