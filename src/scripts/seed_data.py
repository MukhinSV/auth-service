import asyncio

from sqlalchemy import select

from src.database import async_session_maker
from src.models.permissions import PermissionsORM
from src.models.roles import RolesORM
from src.models.roles_permissions import RolesPermissionsORM
from src.models.users import UsersORM
from src.models.users_roles import UsersRolesORM
from src.services.auth import AuthService


TEST_USERS = [
    {
        "firstname": "Admin",
        "lastname": "Root",
        "patronymic": "System",
        "email": "admin@example.com",
        "password": "Admin123!",
        "role": "ADMIN",
    },
    {
        "firstname": "Manager",
        "lastname": "Sales",
        "patronymic": "Team",
        "email": "manager@example.com",
        "password": "Manager123!",
        "role": "MANAGER",
    },
    {
        "firstname": "User",
        "lastname": "Client",
        "patronymic": "Demo",
        "email": "user@example.com",
        "password": "User123!",
        "role": "USER",
    },
]


ROLE_PERMISSIONS = {
    "ADMIN": None,
    "MANAGER": {
        "products.read",
        "products.manage",
    },
    "USER": {
        "products.read",
    },
}


async def seed_roles(session) -> dict[str, RolesORM]:
    role_names = list(ROLE_PERMISSIONS.keys())
    roles_result = await session.execute(
        select(RolesORM).where(RolesORM.role.in_(role_names))
    )
    existing_roles = {role.role: role for role in roles_result.scalars().all()}

    for role_name in role_names:
        if role_name not in existing_roles:
            role = RolesORM(role=role_name)
            session.add(role)
            existing_roles[role_name] = role

    await session.flush()
    return existing_roles


async def seed_permissions_map(session) -> dict[str, PermissionsORM]:
    permissions_result = await session.execute(select(PermissionsORM))
    permissions = permissions_result.scalars().all()
    return {permission.code: permission for permission in permissions}


async def sync_role_permissions(
        session,
        roles: dict[str, RolesORM],
        permissions_by_code: dict[str, PermissionsORM]
) -> None:
    for role_name, permission_codes in ROLE_PERMISSIONS.items():
        role = roles[role_name]
        if permission_codes is None:
            continue

        missing_codes = permission_codes - set(permissions_by_code)
        if missing_codes:
            raise RuntimeError(
                f"Missing permissions for role {role_name}: {sorted(missing_codes)}"
            )

        permissions_result = await session.execute(
            select(RolesPermissionsORM).where(RolesPermissionsORM.role_id == role.id)
        )
        existing_links = permissions_result.scalars().all()
        existing_permission_ids = {
            link.permission_id for link in existing_links
        }
        target_permission_ids = {
            permissions_by_code[code].id for code in permission_codes
        }

        for link in existing_links:
            if link.permission_id not in target_permission_ids:
                await session.delete(link)

        for permission_id in target_permission_ids - existing_permission_ids:
            session.add(
                RolesPermissionsORM(
                    role_id=role.id,
                    permission_id=permission_id,
                )
            )


async def upsert_users(session, roles: dict[str, RolesORM]) -> None:
    emails = [user_data["email"] for user_data in TEST_USERS]
    users_result = await session.execute(
        select(UsersORM).where(UsersORM.email.in_(emails))
    )
    existing_users = {user.email: user for user in users_result.scalars().all()}

    for user_data in TEST_USERS:
        user = existing_users.get(user_data["email"])
        hashed_password = AuthService.pwd_context.hash(user_data["password"])

        if user is None:
            user = UsersORM(
                firstname=user_data["firstname"],
                lastname=user_data["lastname"],
                patronymic=user_data["patronymic"],
                email=user_data["email"],
                hashed_password=hashed_password,
                is_active=True,
            )
            session.add(user)
            await session.flush()
        else:
            user.firstname = user_data["firstname"]
            user.lastname = user_data["lastname"]
            user.patronymic = user_data["patronymic"]
            user.hashed_password = hashed_password
            user.is_active = True

        user_role_result = await session.execute(
            select(UsersRolesORM).where(UsersRolesORM.user_id == user.id)
        )
        user_role = user_role_result.scalars().one_or_none()
        role_id = roles[user_data["role"]].id

        if user_role is None:
            session.add(
                UsersRolesORM(
                    user_id=user.id,
                    role_id=role_id,
                )
            )
        else:
            user_role.role_id = role_id


async def main() -> None:
    async with async_session_maker() as session:
        roles = await seed_roles(session)
        permissions_by_code = await seed_permissions_map(session)
        await sync_role_permissions(session, roles, permissions_by_code)
        await upsert_users(session, roles)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
