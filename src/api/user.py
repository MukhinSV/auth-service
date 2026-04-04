from fastapi import APIRouter, Response

from src.dependencies import UserIdDep, DBDep
from src.exceptions import NoDataForUpdateException, \
    NoDataForUpdateHTTPException
from src.schemas.users import UserUpdatePartly, UserUpdate
from src.services.auth import AuthService
from src.services.users import UserService

router = APIRouter(prefix="/user", tags=["Пользователь"])


@router.get("", summary="Информация о пользователе")
async def get_user(db: DBDep, user_id: UserIdDep):
    return await UserService(db).get_user_with_rels(user_id)


@router.put("", summary="Обновить данные пользователя")
async def update(db: DBDep, user_id: UserIdDep, user_data: UserUpdate):
    await UserService(db).update(user_id, user_data)
    return {"detail": "Данные успешно обновленны"}


@router.patch("", summary="Обновить данные пользователя частично")
async def update_partly(db: DBDep, user_id: UserIdDep,
                        user_data: UserUpdatePartly):
    try:
        await UserService(db).update_partly(user_id, user_data)
        return {"detail": "Данные успешно обновленны"}
    except NoDataForUpdateException:
        raise NoDataForUpdateHTTPException


@router.delete("",
               summary="Удалить пользователя",
               description="Мягко удаляет пользователя, меняет 'is_active' на False."
               )
async def delete_softly(db: DBDep, user_id: UserIdDep, response: Response):
    AuthService().clear_auth_cookies(response)
    await UserService(db).delete_softly(user_id)
    return {"detail": "Пользователь успешно удалён"}
