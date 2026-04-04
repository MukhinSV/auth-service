from src.models.roles_permissions import RolesPermissionsORM
from src.repositories.base import BaseRepository
from src.schemas.roles_permissions import RolesPermissions


class RolesPermissionsRepository(BaseRepository):
    model = RolesPermissionsORM
    schema = RolesPermissions
