"""remove youtube playlists table

Revision ID: 0005
Revises: 0004
Create Date: 2025-11-10 00:00:02.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0005'
down_revision: Union[str, Sequence[str], None] = '0004'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop the playlist_id foreign key constraint and column from youtube_videos
    op.drop_constraint('youtube_videos_playlist_id_fkey', 'youtube_videos', schema='sources', type_='foreignkey')
    op.drop_index(op.f('ix_sources_youtube_videos_playlist_id'), table_name='youtube_videos', schema='sources')
    op.drop_column('youtube_videos', 'playlist_id', schema='sources')
    
    # Drop the youtube_playlists table
    op.drop_index(op.f('ix_sources_youtube_playlists_series_id'), table_name='youtube_playlists', schema='sources')
    op.drop_index(op.f('ix_sources_youtube_playlists_playlist_id'), table_name='youtube_playlists', schema='sources')
    op.drop_index(op.f('ix_sources_youtube_playlists_id'), table_name='youtube_playlists', schema='sources')
    op.drop_table('youtube_playlists', schema='sources')


def downgrade() -> None:
    """Downgrade schema."""
    # Recreate youtube_playlists table
    op.create_table(
        'youtube_playlists',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('playlist_id', sa.String(length=255), nullable=False),
        sa.Column('series_id', sa.Integer(), nullable=False),
        sa.Column('filter_regex', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['series_id'], ['main.series.id'], ),
        sa.PrimaryKeyConstraint('id'),
        schema='sources'
    )
    op.create_index(op.f('ix_sources_youtube_playlists_id'), 'youtube_playlists', ['id'], unique=False, schema='sources')
    op.create_index(op.f('ix_sources_youtube_playlists_playlist_id'), 'youtube_playlists', ['playlist_id'], unique=True, schema='sources')
    op.create_index(op.f('ix_sources_youtube_playlists_series_id'), 'youtube_playlists', ['series_id'], unique=False, schema='sources')
    
    # Add playlist_id column back to youtube_videos
    op.add_column('youtube_videos', sa.Column('playlist_id', sa.Integer(), nullable=False), schema='sources')
    op.create_index(op.f('ix_sources_youtube_videos_playlist_id'), 'youtube_videos', ['playlist_id'], unique=False, schema='sources')
    op.create_foreign_key('youtube_videos_playlist_id_fkey', 'youtube_videos', 'youtube_playlists', ['playlist_id'], ['id'], source_schema='sources', referent_schema='sources')
