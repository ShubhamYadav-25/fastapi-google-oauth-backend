"""Add customer_id to orders

Revision ID: b531464bdedf
Revises: 26ee327705fd
Create Date: 2025-10-18 12:51:41.515326

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b531464bdedf'
down_revision: Union[str, None] = '26ee327705fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
