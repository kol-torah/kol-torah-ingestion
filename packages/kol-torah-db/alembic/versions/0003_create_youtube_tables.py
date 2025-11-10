"""create youtube tables

Revision ID: 0003
Revises: 0002
Create Date: 2025-11-10 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0003'
down_revision: Union[str, Sequence[str], None] = '0002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create youtube_playlists table
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
    
    # Create youtube_videos table
    op.create_table(
        'youtube_videos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('video_id', sa.String(length=255), nullable=False),
        sa.Column('playlist_id', sa.Integer(), nullable=False),
        sa.Column('series_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('publish_date', sa.Date(), nullable=False),
        sa.Column('bucket', sa.String(length=255), nullable=True),
        sa.Column('path', sa.String(length=1000), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['playlist_id'], ['sources.youtube_playlists.id'], ),
        sa.ForeignKeyConstraint(['series_id'], ['main.series.id'], ),
        sa.PrimaryKeyConstraint('id'),
        schema='sources'
    )
    op.create_index(op.f('ix_sources_youtube_videos_id'), 'youtube_videos', ['id'], unique=False, schema='sources')
    op.create_index(op.f('ix_sources_youtube_videos_video_id'), 'youtube_videos', ['video_id'], unique=True, schema='sources')
    op.create_index(op.f('ix_sources_youtube_videos_playlist_id'), 'youtube_videos', ['playlist_id'], unique=False, schema='sources')
    op.create_index(op.f('ix_sources_youtube_videos_series_id'), 'youtube_videos', ['series_id'], unique=False, schema='sources')


def downgrade() -> None:
    """Downgrade schema."""
    # Drop youtube_videos table
    op.drop_index(op.f('ix_sources_youtube_videos_series_id'), table_name='youtube_videos', schema='sources')
    op.drop_index(op.f('ix_sources_youtube_videos_playlist_id'), table_name='youtube_videos', schema='sources')
    op.drop_index(op.f('ix_sources_youtube_videos_video_id'), table_name='youtube_videos', schema='sources')
    op.drop_index(op.f('ix_sources_youtube_videos_id'), table_name='youtube_videos', schema='sources')
    op.drop_table('youtube_videos', schema='sources')
    
    # Drop youtube_playlists table
    op.drop_index(op.f('ix_sources_youtube_playlists_series_id'), table_name='youtube_playlists', schema='sources')
    op.drop_index(op.f('ix_sources_youtube_playlists_playlist_id'), table_name='youtube_playlists', schema='sources')
    op.drop_index(op.f('ix_sources_youtube_playlists_id'), table_name='youtube_playlists', schema='sources')
    op.drop_table('youtube_playlists', schema='sources')
