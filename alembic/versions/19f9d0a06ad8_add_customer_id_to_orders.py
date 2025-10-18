"""Add customer_id to orders

Revision ID: 19f9d0a06ad8
Revises: b531464bdedf
Create Date: 2025-10-18 13:33:59.884875

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '19f9d0a06ad8'
down_revision: Union[str, None] = 'b531464bdedf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
