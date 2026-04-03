from pydantic import BaseModel, ConfigDict


class Role(BaseModel):
    id: int
    user_id: int
    role: str
    model_config = ConfigDict(from_attributes=True)

class RoleRequest(BaseModel):
    user_id: int
    role: str | None = None
