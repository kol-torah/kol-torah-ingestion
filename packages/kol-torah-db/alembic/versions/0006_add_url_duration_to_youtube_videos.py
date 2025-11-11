"""add url and duration to youtube videos

Revision ID: 0006
Revises: 0005
Create Date: 2025-11-11 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0006'
down_revision: Union[str, Sequence[str], None] = '0005'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('youtube_videos', sa.Column('url', sa.String(length=500), nullable=True), schema='sources')
    op.add_column('youtube_videos', sa.Column('duration', sa.Integer(), nullable=True), schema='sources')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('youtube_videos', 'duration', schema='sources')
    op.drop_column('youtube_videos', 'url', schema='sources')
