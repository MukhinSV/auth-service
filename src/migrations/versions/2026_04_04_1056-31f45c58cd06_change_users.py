"""change users

Revision ID: 31f45c58cd06
Revises: 156d8ba361b2
Create Date: 2026-04-04 10:56:41.022352

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "31f45c58cd06"
down_revision: Union[str, Sequence[str], None] = "156d8ba361b2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
