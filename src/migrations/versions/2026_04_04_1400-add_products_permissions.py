"""add products permissions

Revision ID: add_products_permissions
Revises: add_permissions_tables
Create Date: 2026-04-04 14:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "add_products_permissions"
down_revision: Union[str, Sequence[str], None] = "add_permissions_tables"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    permissions_table = sa.table(
        "permissions",
        sa.column("code", sa.String()),
        sa.column("name", sa.String()),
        sa.column("description", sa.String()),
    )
    op.bulk_insert(
        permissions_table,
        [
            {
                "code": "products.read",
                "name": "Просмотр товаров",
                "description": "Позволяет просматривать список товаров и карточки товаров",
            },
            {
                "code": "products.manage",
                "name": "Управление товарами",
                "description": "Позволяет создавать, изменять и удалять товары",
            },
        ]
    )

    op.execute(
        """
        INSERT INTO roles (role)
        SELECT 'MANAGER'
        WHERE NOT EXISTS (
            SELECT 1 FROM roles WHERE role = 'MANAGER'
        )
        """
    )

    op.execute(
        """
        INSERT INTO roles_permissions (role_id, permission_id)
        SELECT roles.id, permissions.id
        FROM roles
        JOIN permissions ON permissions.code = 'products.read'
        WHERE roles.role = 'USER'
        ON CONFLICT (role_id, permission_id) DO NOTHING
        """
    )

    op.execute(
        """
        INSERT INTO roles_permissions (role_id, permission_id)
        SELECT roles.id, permissions.id
        FROM roles
        JOIN permissions ON permissions.code IN ('products.read', 'products.manage')
        WHERE roles.role = 'MANAGER'
        ON CONFLICT (role_id, permission_id) DO NOTHING
        """
    )

    op.execute(
        """
        INSERT INTO roles_permissions (role_id, permission_id)
        SELECT roles.id, permissions.id
        FROM roles
        JOIN permissions ON permissions.code IN ('products.read', 'products.manage')
        WHERE roles.role = 'ADMIN'
        ON CONFLICT (role_id, permission_id) DO NOTHING
        """
    )


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM roles_permissions
        WHERE permission_id IN (
            SELECT id
            FROM permissions
            WHERE code IN ('products.read', 'products.manage')
        )
        """
    )
    op.execute("DELETE FROM roles WHERE role = 'MANAGER'")
    op.execute(
        """
        DELETE FROM permissions
        WHERE code IN ('products.read', 'products.manage')
        """
    )
