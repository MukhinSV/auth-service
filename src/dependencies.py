from typing import Annotated

from fastapi import Depends, Request

from src.database import async_session_maker
from src.exceptions import UserUnauthorisedHTTPException, \
    InvalidTokenException, InvalidTokenHTTPException, \
    AccessDeniedHTTPException, ExpiredTokenException
from src.services.admin import AdminService
from src.services.auth import AuthService
from src.utils.db_manager import DBManager


def get_access_token(request: Request) -> str:
    token = request.cookies.get(AuthService.access_cookie_key, None)
    if not token:
        raise UserUnauthorisedHTTPException
    return token


def get_refresh_token(request: Request) -> str:
    token = request.cookies.get(AuthService.refresh_cookie_key, None)
    if not token:
        raise UserUnauthorisedHTTPException
    return token


def get_current_user_id(access_token: str = Depends(get_access_token)) -> int:
    try:
        access_token_data = AuthService().decode_access_token(access_token)
        return access_token_data["user_id"]
    except InvalidTokenException:
        raise InvalidTokenHTTPException
    except ExpiredTokenException:
        raise UserUnauthorisedHTTPException


async def check_admin(
        db: DBDep,
        user_id: int = Depends(get_current_user_id)
) -> None:
    role = await AdminService(db).get_role(user_id)
    if role.role != "ADMIN":
        raise AccessDeniedHTTPException


UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
