"""make url and duration not nullable in youtube videos

Revision ID: 0007
Revises: 0006
Create Date: 2025-11-11 00:00:01.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0007'
down_revision: Union[str, Sequence[str], None] = '0006'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Make url and duration columns non-nullable
    op.alter_column('youtube_videos', 'url', nullable=False, schema='sources')
    op.alter_column('youtube_videos', 'duration', nullable=False, schema='sources')


def downgrade() -> None:
    """Downgrade schema."""
    # Make url and duration columns nullable again
    op.alter_column('youtube_videos', 'url', nullable=True, schema='sources')
    op.alter_column('youtube_videos', 'duration', nullable=True, schema='sources')
