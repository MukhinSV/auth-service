from fastapi import APIRouter, Depends

from src.dependencies import DBDep, require_permission
from src.exceptions import RoleNotFoundException, UserNotFoundException, \
    UserNotFoundHTTPException, RoleNotFoundHTTPException, \
    RoleCanNotBeDeletedException, RoleCanNotBeDeletedHTTPException, \
    RoleAlreadyExistsHTTPException, PermissionAlreadyExistsHTTPException, \
    PermissionNotFoundException, PermissionNotFoundHTTPException, \
    NoDataForUpdateException, NoDataForUpdateHTTPException
from src.schemas.permissions import PermissionRequest, \
    RolePermissionsUpdateRequest
from src.schemas.roles import RoleRequest
from src.schemas.users import UserUpdatePartlyForAdmin, UserUpdateForAdmin
from src.services.admin import AdminService, RoleAlreadyExistsException, \
    PermissionAlreadyExistsException

router = APIRouter(prefix="/admin", tags=["Администрирование"])


@router.get(
    "/users",
    summary="Получить пользователей",
    dependencies=[Depends(require_permission("users.read"))]
)
async def get_users(db: DBDep):
    return await AdminService(db).get_users()


@router.get(
    "/roles",
    summary="Получить все роли",
    dependencies=[Depends(require_permission("roles.read"))]
)
async def get_roles(db: DBDep):
    return await AdminService(db).get_roles()


@router.get(
    "/permissions",
    summary="Получить все разрешения",
    dependencies=[Depends(require_permission("permissions.read"))]
)
async def get_permissions(db: DBDep):
    return await AdminService(db).get_permissions()


@router.get(
    "/roles/{role_id}/permissions",
    summary="Получить разрешения роли",
    dependencies=[Depends(require_permission("roles.read"))]
)
async def get_role_permissions(db: DBDep, role_id: int):
    try:
        return await AdminService(db).get_role_permissions(role_id)
    except RoleNotFoundException:
        raise RoleNotFoundHTTPException


@router.post(
    "/roles",
    summary="Добавить роль",
    dependencies=[Depends(require_permission("roles.create"))]
)
async def create_roles(db: DBDep, role_data: RoleRequest):
    try:
        await AdminService(db).add_role(role_data)
    except RoleAlreadyExistsException:
        raise RoleAlreadyExistsHTTPException
    return {"detail": "Роль успешно добавлена"}


@router.post(
    "/permissions",
    summary="Добавить разрешение",
    dependencies=[Depends(require_permission("permissions.create"))]
)
async def create_permission(db: DBDep, permission_data: PermissionRequest):
    try:
        await AdminService(db).add_permission(permission_data)
    except PermissionAlreadyExistsException:
        raise PermissionAlreadyExistsHTTPException
    return {"detail": "Разрешение успешно добавлено"}


@router.patch(
    "/users/{user_id}/role",
    summary="Поменять роль пользователя",
    dependencies=[Depends(require_permission("users.update"))]
)
async def change_user_role(db: DBDep, user_id: int, role_id: int):
    try:
        await AdminService(db).change_user_role(user_id, role_id)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    except RoleNotFoundException:
        raise RoleNotFoundHTTPException
    return {"detail": "Роль успешно обновлена"}


@router.put(
    "/users/{user_id}",
    summary="Полностью обновить данные пользователя",
    dependencies=[Depends(require_permission("users.update"))]
)
async def update_user(db: DBDep, user_id: int, user_data: UserUpdateForAdmin):
    try:
        await AdminService(db).update_user(user_id, user_data)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    return {"detail": "Данные пользователя успешно обновлены"}


@router.put(
    "/roles/{role_id}/permissions",
    summary="Обновить разрешения роли",
    dependencies=[Depends(require_permission("roles.update"))]
)
async def set_role_permissions(
        db: DBDep,
        role_id: int,
        permissions_data: RolePermissionsUpdateRequest
):
    try:
        await AdminService(db).set_role_permissions(
            role_id,
            permissions_data.permissions
        )
    except RoleNotFoundException:
        raise RoleNotFoundHTTPException
    except PermissionNotFoundException:
        raise PermissionNotFoundHTTPException
    return {"detail": "Разрешения роли успешно обновлены"}


@router.patch(
    "/users/{user_id}",
    summary="Частично обновить данные пользователя",
    dependencies=[Depends(require_permission("users.update"))]
)
async def update_user_partly(
        db: DBDep,
        user_id: int,
        user_data: UserUpdatePartlyForAdmin
):
    try:
        await AdminService(db).update_user_partly(user_id, user_data)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    except NoDataForUpdateException:
        raise NoDataForUpdateHTTPException
    return {"detail": "Данные пользователя успешно обновлены"}


@router.delete(
    "/users/{user_id}/soft",
    summary="Мягко удалить пользователя",
    description="Меняет поле is_active на False.",
    dependencies=[Depends(require_permission("users.delete"))]
)
async def delete_user_softly(db: DBDep, user_id: int):
    try:
        await AdminService(db).delete_user_softly(user_id)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    return {"detail": "Пользователь успешно мягко удалён"}


@router.delete(
    "/users/{user_id}",
    summary="Полностью удалить пользователя",
    dependencies=[Depends(require_permission("users.delete"))]
)
async def delete_user(db: DBDep, user_id: int):
    try:
        await AdminService(db).delete_user(user_id)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    return {"detail": "Пользователь успешно удалён"}


@router.delete(
    "/roles/{role_id}",
    summary="Удалить роль",
    dependencies=[Depends(require_permission("roles.delete"))],
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
