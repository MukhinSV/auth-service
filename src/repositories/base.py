from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete


class BaseRepository:
    model = None
    schema = BaseModel

    def __init__(self, session):
        self.session = session

    async def get_all(self):
        query = select(self.model)
        results = await self.session.execute(query)
        models = results.scalars().all()
        return [self.schema.model_validate(model) for model in models]

    async def get_one_or_none(self, **filter_by) -> BaseModel | None:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if not model:
            return None
        return self.schema.model_validate(model)

    async def add(self, data: BaseModel, exclude_unset: bool = False):
        add_data_stmt = (insert(self.model)
                         .values(**data.model_dump(exclude_unset=exclude_unset))
                         .returning(self.model))
        result = await self.session.execute(add_data_stmt)
        return result.scalars().one_or_none()

    async def update(
            self,
            data: BaseModel,
            exclude_unset: bool = False,
            **filter_by
    ) -> None:
        update_data_stmt = (
            update(self.model)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .filter_by(**filter_by))
        await self.session.execute(update_data_stmt)

    async def delete(self, **filter_by) -> None:
        delete_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_stmt)
