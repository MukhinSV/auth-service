from pydantic import BaseModel, ConfigDict


class UsersRolesRequest(BaseModel):
    user_id: int
    role_id: int


class UsersRolesUpdate(BaseModel):
    user_id: int | None = None
    role_id: int | None = None


class UsersRoles(BaseModel):
    id: int
    user_id: int
    role_id: int
    model_config = ConfigDict(from_attributes=True)
