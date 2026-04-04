"""add users_roles

Revision ID: 41234976cdc6
Revises: 40fb59cd5655
Create Date: 2026-04-04 10:11:32.695473

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "41234976cdc6"
down_revision: Union[str, Sequence[str], None] = "40fb59cd5655"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(op.f("roles_user_id_fkey"), "roles", type_="foreignkey")
    op.drop_column("roles", "user_id")


def downgrade() -> None:
    op.add_column(
        "roles",
        sa.Column(
            "user_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
    )
    op.create_foreign_key(
        op.f("roles_user_id_fkey"),
        "roles",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
