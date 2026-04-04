"""change users_roles

Revision ID: 592d260eca13
Revises: 31f45c58cd06
Create Date: 2026-04-04 11:19:35.541333

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "592d260eca13"
down_revision: Union[str, Sequence[str], None] = "31f45c58cd06"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users_roles", ["user_id"])


def downgrade() -> None:
    op.drop_constraint(None, "users_roles", type_="unique")
