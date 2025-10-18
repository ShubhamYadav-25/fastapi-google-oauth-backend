"""Initial tables

Revision ID: 26ee327705fd
Revises: 6278937d5397
Create Date: 2025-10-17 17:54:29.294693

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '26ee327705fd'
down_revision: Union[str, None] = '6278937d5397'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
