from pydantic import BaseModel, ConfigDict

from src.schemas.permissions import PermissionResponse


class Role(BaseModel):
    id: int
    role: str
    permissions: list[PermissionResponse] = []
    model_config = ConfigDict(from_attributes=True)


class RoleRequest(BaseModel):
    role: str


class RoleResponse(BaseModel):
    # id: int
    role: str
    permissions: list[PermissionResponse] = []
    model_config = ConfigDict(from_attributes=True)
