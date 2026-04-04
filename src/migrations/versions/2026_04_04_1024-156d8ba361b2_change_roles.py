"""change roles

Revision ID: 156d8ba361b2
Revises: e4d967a6d6bd
Create Date: 2026-04-04 10:24:43.398253

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "156d8ba361b2"
down_revision: Union[str, Sequence[str], None] = "e4d967a6d6bd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
