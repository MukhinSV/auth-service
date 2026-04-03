from fastapi import APIRouter, Response

from src.dependencies import DBDep
from src.exceptions import PasswordNotConfirmedException, \
    PasswordNotConfirmedHTTPException, UserAlreadyExistsException, \
    UserAlreadyExistsHTTPException, WrongEmailOrPasswordException, \
    WrongEmailOrPasswordHTTPException
from src.schemas.users import UserRegisterRequest, UserLoginRequest
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.post("/register", summary="Регистрация")
async def register(db: DBDep, user_data: UserRegisterRequest):
    try:
        return await AuthService(db).register(user_data)
    except PasswordNotConfirmedException:
        raise PasswordNotConfirmedHTTPException
    except UserAlreadyExistsException:
        raise UserAlreadyExistsHTTPException


@router.post("/login", summary="Вход")
async def login(db: DBDep, user_data: UserLoginRequest, response: Response):
    try:
        tokens = await AuthService(db).login(user_data)
        response.set_cookie("access_token", tokens["access_token"])
        response.set_cookie( "refresh_token", tokens["refresh_token"])
        return tokens
    except WrongEmailOrPasswordException:
        raise WrongEmailOrPasswordHTTPException


@router.post("/logout", summary="Выход")
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"detail": "Успешный выход"}
