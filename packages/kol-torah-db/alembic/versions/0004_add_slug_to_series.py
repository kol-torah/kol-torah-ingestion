"""add slug to series

Revision ID: 0004
Revises: 0003
Create Date: 2025-11-10 00:00:01.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0004'
down_revision: Union[str, Sequence[str], None] = '0003'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add slug column as nullable first
    op.add_column('series', sa.Column('slug', sa.String(length=255), nullable=True), schema='main')
    
    # Generate slug values for existing rows (if any)
    # This uses a simple approach: lowercase name_english with spaces replaced by hyphens
    op.execute("""
        UPDATE main.series 
        SET slug = LOWER(REPLACE(name_english, ' ', '-'))
        WHERE slug IS NULL
    """)
    
    # Now make the column non-nullable
    op.alter_column('series', 'slug', nullable=False, schema='main')
    
    # Add unique constraint and index
    op.create_index(op.f('ix_main_series_slug'), 'series', ['slug'], unique=True, schema='main')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_main_series_slug'), table_name='series', schema='main')
    op.drop_column('series', 'slug', schema='main')
