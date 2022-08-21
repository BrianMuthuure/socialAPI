"""add content column to posts table

Revision ID: 8dfe0e0315e1
Revises: c3adc902db09
Create Date: 2022-08-19 11:22:50.597548

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8dfe0e0315e1'
down_revision = 'c3adc902db09'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
