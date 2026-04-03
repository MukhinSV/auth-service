from pydantic import BaseModel, EmailStr, ConfigDict


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


class UserUpdatePartly(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    patronymic: str | None = None
    email: EmailStr | None = None
    is_active: bool | None = None


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
    model_config = ConfigDict(from_attributes=True)

class UserWithHashedPassword(User):
    hashed_password: str
    model_config = ConfigDict(from_attributes=True)
