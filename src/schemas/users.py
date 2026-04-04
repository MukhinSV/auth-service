from pydantic import BaseModel, EmailStr, ConfigDict

from src.schemas.roles import Role, RoleResponse


class UserRegisterRequest(BaseModel):
    firstname: str
    lastname: str
    patronymic: str
    email: EmailStr
    password: str
    password_confirmation: str


class UserRegister(BaseModel):
    firstname: str
    lastname: str
    patronymic: str
    email: EmailStr
    hashed_password: str


class UserUpdatePartlyForAdmin(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    patronymic: str | None = None
    email: EmailStr | None = None
    is_active: bool | None = None


class UserUpdatePartly(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    patronymic: str | None = None
    email: EmailStr | None = None


class UserUpdate(BaseModel):
    firstname: str
    lastname: str
    patronymic: str
    email: EmailStr


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    firstname: str
    lastname: str
    patronymic: str
    email: EmailStr
    is_active: bool
    roles: RoleResponse
    model_config = ConfigDict(from_attributes=True)

class UserWithHashedPassword(User):
    hashed_password: str
    model_config = ConfigDict(from_attributes=True)
