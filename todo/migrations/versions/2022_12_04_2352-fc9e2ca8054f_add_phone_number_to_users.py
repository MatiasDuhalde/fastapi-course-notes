"""add phone number to users

Revision ID: fc9e2ca8054f
Revises: 
Create Date: 2022-12-04 23:52:18.596595

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'fc9e2ca8054f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(length=20), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
