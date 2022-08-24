"""create posts table

Revision ID: c3adc902db09
Revises:
Create Date: 2022-08-19 11:05:46.649355

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3adc902db09'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column(
            'id',
            sa.Integer(),
            nullable=False,
            primary_key=True),
        sa.Column(
            'title',
            sa.String(),
            nullable=False))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
