from sqlalchemy import select

from src.models.permissions import PermissionsORM
from src.repositories.base import BaseRepository
from src.schemas.permissions import Permission


class PermissionsRepository(BaseRepository):
    model = PermissionsORM
    schema = Permission

    async def get_all_by_codes(self, codes: list[str]) -> list[Permission]:
        if not codes:
            return []
        query = select(self.model).where(self.model.code.in_(codes))
        results = await self.session.execute(query)
        models = results.scalars().all()
        return [self.schema.model_validate(model) for model in models]
