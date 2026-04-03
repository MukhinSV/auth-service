"""change users and roles

Revision ID: 0008431860fe
Revises: d5d54c957e2c
Create Date: 2026-04-03 10:20:33.019537

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0008431860fe"
down_revision: Union[str, Sequence[str], None] = "d5d54c957e2c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("lastname", sa.String(), nullable=False))
    op.drop_column("users", "surname")


def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "surname", sa.VARCHAR(), autoincrement=False, nullable=False
        ),
    )
    op.drop_column("users", "lastname")
