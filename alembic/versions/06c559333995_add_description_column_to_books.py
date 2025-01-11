"""Add description column to books

Revision ID: 06c559333995
Revises: 17b841505634
Create Date: 2025-01-11 23:14:20.082736

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '06c559333995'
down_revision: Union[str, None] = '17b841505634'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('books', sa.Column('description', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('books', 'description')