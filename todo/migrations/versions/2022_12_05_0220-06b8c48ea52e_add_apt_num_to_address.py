"""add apt_num to address

Revision ID: 06b8c48ea52e
Revises: 69ab0cb1c297
Create Date: 2022-12-05 02:20:40.285083

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '06b8c48ea52e'
down_revision = '69ab0cb1c297'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('address', sa.Column('apt_num', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('address', 'apt_num')
