from fastapi import APIRouter

from src.dependencies import UserIdDep, DBDep
from src.services.users import UserService

router = APIRouter(prefix="/user", tags=["Пользователь"])

@router.get("", summary="Информация о пользователе")
async def get_user(db: DBDep, user_id: UserIdDep):
    return await UserService(db).get_user(user_id)
