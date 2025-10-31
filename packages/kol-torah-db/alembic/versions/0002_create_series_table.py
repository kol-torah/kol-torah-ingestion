"""create series table

Revision ID: 0002
Revises: 0001
Create Date: 2025-10-31 12:00:01.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0002'
down_revision: Union[str, Sequence[str], None] = '0001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'series',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('rabbi_id', sa.Integer(), nullable=False),
        sa.Column('name_hebrew', sa.String(length=255), nullable=False),
        sa.Column('name_english', sa.String(length=255), nullable=False),
        sa.Column('description_hebrew', sa.Text(), nullable=True),
        sa.Column('description_english', sa.Text(), nullable=True),
        sa.Column('website_url', sa.String(length=500), nullable=True),
        sa.Column('type', sa.String(length=100), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['rabbi_id'], ['main.rabbis.id'], ),
        sa.PrimaryKeyConstraint('id'),
        schema='main'
    )
    op.create_index(op.f('ix_main_series_id'), 'series', ['id'], unique=False, schema='main')
    op.create_index(op.f('ix_main_series_rabbi_id'), 'series', ['rabbi_id'], unique=False, schema='main')
    op.create_index(op.f('ix_main_series_type'), 'series', ['type'], unique=False, schema='main')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_main_series_type'), table_name='series', schema='main')
    op.drop_index(op.f('ix_main_series_rabbi_id'), table_name='series', schema='main')
    op.drop_index(op.f('ix_main_series_id'), table_name='series', schema='main')
    op.drop_table('series', schema='main')
