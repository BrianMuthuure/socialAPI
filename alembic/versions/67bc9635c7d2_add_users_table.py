"""add users table

Revision ID: 67bc9635c7d2
Revises: 8dfe0e0315e1
Create Date: 2022-08-19 11:35:15.341017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '67bc9635c7d2'
down_revision = '8dfe0e0315e1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
