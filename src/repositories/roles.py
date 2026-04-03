from src.models.roles import RolesORM
from src.repositories.base import BaseRepository
from src.schemas.roles import Role


class RolesRepository(BaseRepository):
    model = RolesORM
    schema = Role
