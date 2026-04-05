from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models.roles import RolesORM
from src.models.users import UsersORM
from src.repositories.base import BaseRepository
from src.schemas.users import User, UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersORM
    schema = User

    async def get_one_or_none(self, **filter_by) -> BaseModel | None:
        query = (select(self.model)
                 .options(
            selectinload(self.model.roles)
            .selectinload(RolesORM.permissions)
        )
                 .filter_by(**filter_by))
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if not model:
            return None
        return self.schema.model_validate(model)

    async def get_all_with_rels(self):
        query = select(self.model).options(
            selectinload(self.model.roles).selectinload(RolesORM.permissions)
        )
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [self.schema.model_validate(model) for model in models]

    async def get_user_with_hashed_password(
            self,
            **filter_by
    ) -> BaseModel | None:
        query = (select(self.model)
                 .options(
            selectinload(self.model.roles)
            .selectinload(RolesORM.permissions)
        )
                 .filter_by(**filter_by))
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if not model:
            return None
        return UserWithHashedPassword.model_validate(model)

    async def get_one_or_none_with_rels(self, **filter_by) -> BaseModel | None:
        query = (select(self.model)
                 .options(
            selectinload(self.model.roles)
            .selectinload(RolesORM.permissions)
        )
                 .filter_by(**filter_by))
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if not model:
            return None
        return self.schema.model_validate(model)
