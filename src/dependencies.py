from typing import Annotated

from fastapi import Depends, Request, Response

from src.database import async_session_maker
from src.exceptions import UserUnauthorisedHTTPException, \
    InvalidTokenException, InvalidTokenHTTPException, \
    AccessDeniedHTTPException, ExpiredTokenException
from src.services.admin import AdminService
from src.services.auth import AuthService
from src.utils.db_manager import DBManager


def get_access_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise UserUnauthorisedHTTPException
    return token


def get_refresh_token(request: Request) -> str:
    token = request.cookies.get("refresh_token", None)
    if not token:
        raise UserUnauthorisedHTTPException
    return token


def get_current_user_id(
        response: Response,
        access_token: str = Depends(get_access_token),
        refresh_token: str = Depends(get_refresh_token),
) -> int:
    try:
        access_token_data = AuthService().decode_token(access_token)
        return access_token_data["user_id"]
    except InvalidTokenException:
        raise InvalidTokenHTTPException
    except ExpiredTokenException:
        try:
            refresh_token_data = AuthService().decode_token(refresh_token)
            new_access_token = AuthService().create_access_token(
                {"user_id": refresh_token_data["user_id"]})
            new_refresh_token = AuthService().create_refresh_token(
                {"user_id": refresh_token_data["user_id"]})
            response.set_cookie("access_token", new_access_token)
            response.set_cookie("refresh_token", new_refresh_token)
            return refresh_token_data["user_id"]
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
