"""add users_roles

Revision ID: e4d967a6d6bd
Revises: 41234976cdc6
Create Date: 2026-04-04 10:13:06.743266

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "e4d967a6d6bd"
down_revision: Union[str, Sequence[str], None] = "41234976cdc6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users_roles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roles.id"],
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users_roles")
