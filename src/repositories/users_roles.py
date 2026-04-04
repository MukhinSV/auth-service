from src.models.users_roles import UsersRolesORM
from src.repositories.base import BaseRepository
from src.schemas.users_roles import UsersRoles


class UsersRolesRepository(BaseRepository):
    model = UsersRolesORM
    schema = UsersRoles
