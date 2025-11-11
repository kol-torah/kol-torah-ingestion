"""add transcript fields to youtube videos

Revision ID: 0008
Revises: 0007
Create Date: 2025-11-11 00:00:02.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0008'
down_revision: Union[str, Sequence[str], None] = '0007'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('youtube_videos', sa.Column('transcript_bucket', sa.String(length=255), nullable=True), schema='sources')
    op.add_column('youtube_videos', sa.Column('transcript_path', sa.String(length=1000), nullable=True), schema='sources')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('youtube_videos', 'transcript_path', schema='sources')
    op.drop_column('youtube_videos', 'transcript_bucket', schema='sources')
