from pydantic import BaseModel
from sqlalchemy import select, insert, update


class BaseRepository:
    model = None
    schema = BaseModel

    def __init__(self, session):
        self.session = session

    async def get_one_or_none(self, **filter_by) -> BaseModel | None:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if not model:
            return None
        return self.schema.model_validate(model)

    async def add(self, data: BaseModel, exclude_unset: bool = False) -> BaseModel:
        add_data_stmt = (insert(self.model)
                         .values(**data.model_dump(exclude_unset=exclude_unset))
                         .returning(self.model))
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()
        return self.schema.model_validate(model)

    async def update(
            self,
            data: BaseModel,
            exclude_unset: bool = False,
            **filter_by
    ) -> BaseModel:
        update_data_stmt = (update(self.model)
                            .values(**data.model_dump(exclude_unset=exclude_unset)).
                            filter_by(**filter_by)
                            .returning(self.model))
        result = await self.session.execute(update_data_stmt)
        model = result.scalars().one()
        return self.schema.model_validate(model)
