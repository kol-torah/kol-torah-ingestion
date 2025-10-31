"""create rabbis table

Revision ID: 0001
Revises: 
Create Date: 2025-10-31 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0001'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'rabbis',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name_hebrew', sa.String(length=255), nullable=False),
        sa.Column('name_english', sa.String(length=255), nullable=False),
        sa.Column('slug', sa.String(length=255), nullable=False),
        sa.Column('website_url', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema='main'
    )
    op.create_index(op.f('ix_main_rabbis_id'), 'rabbis', ['id'], unique=False, schema='main')
    op.create_index(op.f('ix_main_rabbis_name_english'), 'rabbis', ['name_english'], unique=False, schema='main')
    op.create_index(op.f('ix_main_rabbis_name_hebrew'), 'rabbis', ['name_hebrew'], unique=False, schema='main')
    op.create_index(op.f('ix_main_rabbis_slug'), 'rabbis', ['slug'], unique=True, schema='main')


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_main_rabbis_slug'), table_name='rabbis', schema='main')
    op.drop_index(op.f('ix_main_rabbis_name_hebrew'), table_name='rabbis', schema='main')
    op.drop_index(op.f('ix_main_rabbis_name_english'), table_name='rabbis', schema='main')
    op.drop_index(op.f('ix_main_rabbis_id'), table_name='rabbis', schema='main')
    op.drop_table('rabbis', schema='main')
