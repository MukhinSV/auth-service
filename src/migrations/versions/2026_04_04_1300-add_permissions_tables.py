"""add permissions tables

Revision ID: add_permissions_tables
Revises: 592d260eca13
Create Date: 2026-04-04 13:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "add_permissions_tables"
down_revision: Union[str, Sequence[str], None] = "592d260eca13"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


PERMISSIONS = [
    ("users.read", "Просмотр пользователей", "Позволяет просматривать список пользователей"),
    ("users.update", "Изменение пользователей", "Позволяет менять роль пользователя"),
    ("users.delete", "Удаление пользователей", "Зарезервировано для операций удаления пользователей"),
    ("roles.read", "Просмотр ролей", "Позволяет просматривать список ролей"),
    ("roles.create", "Создание ролей", "Позволяет создавать новые роли"),
    ("roles.update", "Изменение ролей", "Позволяет настраивать разрешения ролей"),
    ("roles.delete", "Удаление ролей", "Позволяет удалять роли"),
    ("permissions.read", "Просмотр разрешений", "Позволяет просматривать справочник разрешений"),
    ("permissions.create", "Создание разрешений", "Позволяет создавать новые разрешения"),
]


def upgrade() -> None:
    op.create_table(
        "permissions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_table(
        "roles_permissions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("permission_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["permission_id"], ["permissions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("role_id", "permission_id"),
    )

    permissions_table = sa.table(
        "permissions",
        sa.column("code", sa.String()),
        sa.column("name", sa.String()),
        sa.column("description", sa.String()),
    )
    op.bulk_insert(
        permissions_table,
        [
            {"code": code, "name": name, "description": description}
            for code, name, description in PERMISSIONS
        ]
    )

    op.execute(
        """
        INSERT INTO roles_permissions (role_id, permission_id)
        SELECT roles.id, permissions.id
        FROM roles
        CROSS JOIN permissions
        WHERE roles.role = 'ADMIN'
        """
    )


def downgrade() -> None:
    op.drop_table("roles_permissions")
    op.drop_table("permissions")
