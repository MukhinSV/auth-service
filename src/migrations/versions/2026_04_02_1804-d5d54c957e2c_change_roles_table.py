"""change roles table

Revision ID: d5d54c957e2c
Revises: e56514c4fc34
Create Date: 2026-04-02 18:04:46.617135

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "d5d54c957e2c"
down_revision: Union[str, Sequence[str], None] = "e56514c4fc34"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "roles", ["role"])


def downgrade() -> None:
    op.drop_constraint(None, "roles", type_="unique")
