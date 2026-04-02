"""add tables users, roles

Revision ID: 788cdedb8dd4
Revises:
Create Date: 2026-04-02 17:58:52.204586

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "788cdedb8dd4"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("firstname", sa.String(), nullable=False),
        sa.Column("surname", sa.String(), nullable=False),
        sa.Column("patronymic", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("roles")
    op.drop_table("users")
