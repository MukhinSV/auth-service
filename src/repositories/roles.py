from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models.roles import RolesORM
from src.repositories.base import BaseRepository
from src.schemas.roles import Role


class RolesRepository(BaseRepository):
    model = RolesORM
    schema = Role

    async def get_all(self):
        return await self.get_all_with_permissions()

    async def get_one_or_none(self, **filter_by):
        return await self.get_one_or_none_with_permissions(**filter_by)

    async def get_all_with_permissions(self):
        query = select(self.model).options(
            selectinload(self.model.permissions))
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [self.schema.model_validate(model) for model in models]

    async def get_one_or_none_with_permissions(self, **filter_by):
        query = (select(self.model)
                 .options(selectinload(self.model.permissions))
                 .filter_by(**filter_by))
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if not model:
            return None
        return self.schema.model_validate(model)
