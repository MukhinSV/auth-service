from src.exceptions import UserNotFoundException, RoleNotFoundException, \
    RoleCanNotBeDeletedException, RoleAlreadyExistsException, \
    PermissionAlreadyExistsException, PermissionNotFoundException, \
    NoDataForUpdateException, UserAlreadyExistsException
from src.schemas.permissions import Permission, PermissionRequest
from src.schemas.roles import Role, RoleRequest
from src.schemas.roles_permissions import RolesPermissionsRequest
from src.schemas.users import User, UserUpdatePartlyForAdmin, \
    UserUpdateForAdmin
from src.schemas.users_roles import UsersRolesUpdate
from src.services.base import BaseService


class AdminService(BaseService):
    async def get_users(self) -> list[User]:
        return await self.db.users.get_all_with_rels()

    async def get_user(self, user_id: int) -> User:
        user = await self.db.users.get_one_or_none_with_rels(id=user_id)
        if user is None:
            raise UserNotFoundException
        return user

    async def get_role(self, role_id: int) -> Role:
        return await self.db.roles.get_one_or_none_with_permissions(id=role_id)

    async def get_roles(self) -> list[Role]:
        return await self.db.roles.get_all_with_permissions()

    async def add_role(self, role_data: RoleRequest):
        role = await self.db.roles.get_one_or_none(role=role_data.role)
        if role:
            raise RoleAlreadyExistsException
        await self.db.roles.add(role_data)
        await self.db.commit()

    async def change_user_role(self, user_id: int, role_id: int):
        user = await self.db.users.get_one_or_none_with_rels(id=user_id)
        if user is None or user.is_active is False:
            raise UserNotFoundException
        role = await self.db.roles.get_one_or_none(id=role_id)
        if role is None:
            raise RoleNotFoundException
        await self.db.users_roles.update(
            UsersRolesUpdate(role_id=role_id),
            exclude_unset=True,
            user_id=user_id
        )
        await self.db.commit()

    async def update_user(
            self,
            user_id: int,
            user_data: UserUpdateForAdmin
    ) -> None:
        user = await self.db.users.get_one_or_none_with_rels(email=user_data.email)
        if user:
            raise UserAlreadyExistsException
        user = await self.db.users.get_one_or_none(id=user_id)
        if user is None:
            raise UserNotFoundException
        await self.db.users.update(user_data, id=user_id)
        await self.db.commit()

    async def update_user_partly(
            self,
            user_id: int,
            user_data: UserUpdatePartlyForAdmin
    ) -> None:
        user = await self.db.users.get_one_or_none_with_rels(email=user_data.email)
        if user:
            raise UserAlreadyExistsException
        user = await self.db.users.get_one_or_none(id=user_id)
        if user is None:
            raise UserNotFoundException
        if not user_data.model_dump(exclude_unset=True):
            raise NoDataForUpdateException
        await self.db.users.update(
            user_data,
            exclude_unset=True,
            id=user_id
        )
        await self.db.commit()

    async def delete_user_softly(self, user_id: int) -> None:
        user = await self.db.users.get_one_or_none(id=user_id)
        if user is None:
            raise UserNotFoundException
        await self.db.users.update(
            UserUpdatePartlyForAdmin(is_active=False),
            exclude_unset=True,
            id=user_id
        )
        await self.db.commit()

    async def delete_user(self, user_id: int) -> None:
        user = await self.db.users.get_one_or_none(id=user_id)
        if user is None:
            raise UserNotFoundException
        await self.db.users.delete(id=user_id)
        await self.db.commit()

    async def delete_role(self, role_id: int):
        role = await self.db.roles.get_one_or_none(id=role_id)
        if role is None:
            raise RoleNotFoundException
        if role.role == "USER" or role.role == "ADMIN":
            raise RoleCanNotBeDeletedException
        user_role = await self.db.roles.get_one_or_none(role="USER")
        user_role_id = user_role.id
        await self.db.users_roles.update(
            UsersRolesUpdate(role_id=user_role_id),
            exclude_unset=True,
            role_id=role.id
        )
        await self.db.roles.delete(id=role.id)
        await self.db.commit()

    async def get_permissions(self) -> list[Permission]:
        return await self.db.permissions.get_all()

    async def add_permission(self, permission_data: PermissionRequest):
        permission = await self.db.permissions.get_one_or_none(
            code=permission_data.code
        )
        if permission:
            raise PermissionAlreadyExistsException
        await self.db.permissions.add(permission_data)
        await self.db.commit()

    async def get_role_permissions(self, role_id: int) -> list[Permission]:
        role = await self.db.roles.get_one_or_none_with_permissions(id=role_id)
        if role is None:
            raise RoleNotFoundException
        return role.permissions

    async def set_role_permissions(
            self,
            role_id: int,
            permission_codes: list[str]
    ) -> None:
        role = await self.db.roles.get_one_or_none(id=role_id)
        if role is None:
            raise RoleNotFoundException

        permissions = await self.db.permissions.get_all_by_codes(
            permission_codes)
        found_codes = {permission.code for permission in permissions}
        missing_codes = set(permission_codes) - found_codes
        if missing_codes:
            raise PermissionNotFoundException

        await self.db.roles_permissions.delete(role_id=role_id)
        for permission in permissions:
            await self.db.roles_permissions.add(
                RolesPermissionsRequest(
                    role_id=role_id,
                    permission_id=permission.id
                )
            )
        await self.db.commit()
