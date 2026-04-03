from typing import Annotated

from fastapi import Depends, Request

from src.database import async_session_maker
from src.exceptions import UserUnauthorisedHTTPException, \
    InvalidTokenException, InvalidTokenHTTPException, AccessDeniedHTTPException
from src.services.admin import AdminService
from src.services.auth import AuthService
from src.utils.db_manager import DBManager


def get_access_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise UserUnauthorisedHTTPException
    return token


def get_current_user_id(token: str = Depends(get_access_token)) -> int:
    try:
        data = AuthService().decode_token(token)
    except InvalidTokenException:
        raise InvalidTokenHTTPException
    return data["user_id"]


async def check_admin(db: DBDep, token: str = Depends(get_access_token)) -> None:
    try:
        data = AuthService().decode_token(token)
    except InvalidTokenException:
        raise InvalidTokenHTTPException
    role = await AdminService(db).get_role(data["user_id"])
    if role.role != "ADMIN":
        raise AccessDeniedHTTPException


UserIdDep = Annotated[int, Depends(get_current_user_id)]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]
