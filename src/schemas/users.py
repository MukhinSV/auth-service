from pydantic import BaseModel, EmailStr


class UserRegisterRequest(BaseModel):
    firstname: str
    lastname: str
    patronymic: str
    email: EmailStr
    password: str
    repeated_password: str


class UserRegister(BaseModel):
    firstname: str
    lastname: str
    patronymic: str
    email: EmailStr
    hashed_password: str


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    firstname: str
    lastname: str
    patronymic: str
    email: EmailStr
