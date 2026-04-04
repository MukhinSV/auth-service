from typing import Annotated

from fastapi import Depends, Request

from src.database import async_session_maker
from src.exceptions import UserUnauthorisedHTTPException, \
    InvalidTokenException, InvalidTokenHTTPException, \
    AccessDeniedHTTPException, ExpiredTokenException
from src.services.auth import AuthService
from src.services.users import UserService
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


def require_permission(permission_code: str):
    async def checker(
            db: DBDep,
            user_id: int = Depends(get_current_user_id)
    ) -> None:
        user = await UserService(db).get_user_with_rels(user_id)
        if user is None:
            raise UserUnauthorisedHTTPException
        if user.roles.role == "ADMIN":
            return
        user_permissions = {permission.code for permission in
                            user.roles.permissions}
        if permission_code not in user_permissions:
            raise AccessDeniedHTTPException

    return checker


UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
