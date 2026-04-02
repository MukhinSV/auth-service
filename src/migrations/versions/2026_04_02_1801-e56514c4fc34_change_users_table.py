"""change users table

Revision ID: e56514c4fc34
Revises: 788cdedb8dd4
Create Date: 2026-04-02 18:01:35.056054

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "e56514c4fc34"
down_revision: Union[str, Sequence[str], None] = "788cdedb8dd4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
