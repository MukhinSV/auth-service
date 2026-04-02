from fastapi import APIRouter

from src.dependencies import DBDep
from src.exceptions import PasswordsNotEqualException, \
    PasswordsNotEqualHTTPException
from src.schemas.users import UserRegisterRequest
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.post("/register", summary="Регистрация")
async def register(db: DBDep, user_data: UserRegisterRequest):
    try:
        await AuthService(db).register(user_data)
    except PasswordsNotEqualException:
        raise PasswordsNotEqualHTTPException


@router.post("/login", summary="Вход")
async def login():
    pass


@router.post("/logout", summary="Выход")
async def logout():
    pass
