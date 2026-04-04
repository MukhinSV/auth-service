from src.exceptions import UserNotFoundException, RoleNotFoundException, \
    RoleCanNotBeDeletedException, RoleAlreadyExistsException
from src.schemas.roles import Role, RoleRequest
from src.schemas.users import User
from src.schemas.users_roles import UsersRolesRequest, UsersRolesUpdate
from src.services.base import BaseService


class AdminService(BaseService):
    async def get_users(self) -> list[User]:
        return await self.db.users.get_all_with_rels()

    async def get_role(self, user_id: int) -> Role:
        return await self.db.roles.get_one_or_none(user_id=user_id)

    async def get_roles(self) -> list[Role]:
        return await self.db.roles.get_all()

    async def add_role(self, role_data: RoleRequest):
        role = await self.db.roles.get_one_or_none(role=role_data.role)
        if role:
            raise RoleAlreadyExistsException
        await self.db.roles.add(role_data)
        await self.db.commit()

    async def change_user_role(self, user_id: int, role_id: int):
        user = await self.db.users.get_one_or_none_with_rels(id=user_id)
        if user is None or user.is_active == False:
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

    async def delete_role(self, role_id: int):
        role = await self.db.roles.get_one_or_none(id=role_id)
        print(role)
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