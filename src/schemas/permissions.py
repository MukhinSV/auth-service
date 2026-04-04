from pydantic import BaseModel, ConfigDict


class Permission(BaseModel):
    id: int
    code: str
    name: str
    description: str | None = None
    model_config = ConfigDict(from_attributes=True)


class PermissionRequest(BaseModel):
    code: str
    name: str
    description: str | None = None


class PermissionResponse(BaseModel):
    # id: int
    code: str
    name: str
    description: str | None = None
    model_config = ConfigDict(from_attributes=True)


class RolePermissionsUpdateRequest(BaseModel):
    permissions: list[str]
