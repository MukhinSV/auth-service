from pydantic import BaseModel


class RolesPermissionsRequest(BaseModel):
    role_id: int
    permission_id: int


class RolesPermissions(BaseModel):
    id: int
    role_id: int
    permission_id: int
