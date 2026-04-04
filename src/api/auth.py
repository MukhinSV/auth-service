from fastapi import APIRouter, Body, Depends, Response, Request
from fastapi.openapi.models import Example

from src.dependencies import DBDep, get_refresh_token, get_current_user_id
from src.exceptions import PasswordNotConfirmedException, \
    PasswordNotConfirmedHTTPException, UserAlreadyExistsException, \
    UserAlreadyExistsHTTPException, WrongEmailOrPasswordException, \
    WrongEmailOrPasswordHTTPException, InvalidTokenException, \
    InvalidTokenHTTPException, ExpiredTokenException, \
    UserUnauthorisedHTTPException
from src.schemas.users import UserRegisterRequest, UserLoginRequest
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Аутентификация и авторизация"])


@router.post("/register", summary="Регистрация", status_code=201)
async def register(db: DBDep, user_data: UserRegisterRequest):
    try:
        await AuthService(db).register(user_data)
        return {"detail": "Успешная регистрация"}
    except PasswordNotConfirmedException:
        raise PasswordNotConfirmedHTTPException
    except UserAlreadyExistsException:
        raise UserAlreadyExistsHTTPException


@router.post("/login", summary="Вход")
async def login(
        db: DBDep,
        response: Response,
        request: Request,
        user_data: UserLoginRequest = Body(
            openapi_examples={
                "admin": Example(
                    summary="Вход как ADMIN",
                    value={
                        "email": "admin@example.com",
                        "password": "Admin123!",
                    },
                ),
                "manager": Example(
                    summary="Вход как MANAGER",
                    value={
                        "email": "manager@example.com",
                        "password": "Manager123!",
                    },
                ),
                "user": Example(
                    summary="Вход как USER",
                    value={
                        "email": "user@example.com",
                        "password": "User123!",
                    },
                ),
            }
        )
):
    try:
        tokens = await AuthService(db).login(user_data)
        AuthService.set_auth_cookies(response, tokens)
        return {"detail": "Успешный вход"}
    except WrongEmailOrPasswordException:
        raise WrongEmailOrPasswordHTTPException


@router.post("/refresh",
             summary="Обновление токенов",
             description="""
             Обновляет access token, если refresh token ещё не истёк.
             Если refresh token истёк, пользователь должен заново войти в аккаунт.
             """
             )
async def refresh_tokens(
        response: Response,
        refresh_token: str = Depends(get_refresh_token),
):
    try:
        tokens = AuthService().refresh(refresh_token)
        AuthService.set_auth_cookies(response, tokens)
        return {"detail": "Токены обновлены"}
    except InvalidTokenException:
        raise InvalidTokenHTTPException
    except ExpiredTokenException:
        raise UserUnauthorisedHTTPException


@router.post("/logout", summary="Выход",
             dependencies=[Depends(get_current_user_id)])
async def logout(response: Response):
    AuthService.clear_auth_cookies(response)
    return {"detail": "Успешный выход"}
