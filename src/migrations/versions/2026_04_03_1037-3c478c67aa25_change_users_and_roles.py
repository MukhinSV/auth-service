"""change users and roles

Revision ID: 3c478c67aa25
Revises: 0008431860fe
Create Date: 2026-04-03 10:37:39.211545

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "3c478c67aa25"
down_revision: Union[str, Sequence[str], None] = "0008431860fe"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(op.f("roles_user_id_fkey"), "roles", type_="foreignkey")
    op.create_foreign_key(
        None, "roles", "users", ["user_id"], ["id"], ondelete="CASCADE"
    )
    op.add_column(
        "users", sa.Column("is_active", sa.Boolean(), nullable=False)
    )


def downgrade() -> None:
    op.drop_column("users", "is_active")
    op.drop_constraint(None, "roles", type_="foreignkey")
    op.create_foreign_key(
        op.f("roles_user_id_fkey"), "roles", "users", ["user_id"], ["id"]
    )
