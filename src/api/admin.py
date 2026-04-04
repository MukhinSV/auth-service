from fastapi import APIRouter, Depends

from src.dependencies import DBDep, check_admin
from src.exceptions import RoleNotFoundException, UserNotFoundException, \
    UserNotFoundHTTPException, RoleNotFoundHTTPException, \
    RoleCanNotBeDeletedException, RoleCanNotBeDeletedHTTPException, \
    RoleAlreadyExistsHTTPException
from src.schemas.roles import RoleRequest
from src.services.admin import AdminService, RoleAlreadyExistsException

router = APIRouter(prefix="/admin", tags=["Администрирование"], dependencies=[Depends(check_admin)])

@router.get("/users", summary="Получить пользователей")
async def get_users(db: DBDep):
    return await AdminService(db).get_users()


@router.get("/roles", summary="Получить все роли")
async def get_roles(db: DBDep):
    return await AdminService(db).get_roles()


@router.post("/roles", summary="Добавить роль")
async def create_roles(db: DBDep, role_data: RoleRequest):
    try:
        await AdminService(db).add_role(role_data)
    except RoleAlreadyExistsException:
        raise RoleAlreadyExistsHTTPException
    return {"detail": "Роль успешно добавлена"}


@router.patch("/users/{user_id}", summary="Поменять роль пользователя")
async def change_user_role(db: DBDep, user_id: int, role_id: int):
    try:
        await AdminService(db).change_user_role(user_id, role_id)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    except RoleNotFoundException:
        raise RoleNotFoundHTTPException
    return {"detail": "Роль успешно обновлена"}


@router.delete(
    "/roles/{role_id}",
    summary="Удалить роль",
    description="""
    При удалении роли все пользователи, которые ей обладали, получают роль 'USER'.
    Роли 'USER' и 'ADMIN' удалить нельзя.
    """
)
async def delete_role(db: DBDep, role_id: int):
    try:
        await AdminService(db).delete_role(role_id)
    except RoleNotFoundException:
        raise RoleNotFoundHTTPException
    except RoleCanNotBeDeletedException:
        raise RoleCanNotBeDeletedHTTPException
    return {"detail": "Роль успешно удалена"}
