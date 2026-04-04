from pydantic import BaseModel, ConfigDict


class Role(BaseModel):
    id: int
    role: str
    model_config = ConfigDict(from_attributes=True)


class RoleRequest(BaseModel):
    role: str


class RoleResponse(BaseModel):
    role: str
    model_config = ConfigDict(from_attributes=True)
