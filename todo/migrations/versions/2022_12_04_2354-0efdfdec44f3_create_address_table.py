"""create address table

Revision ID: 0efdfdec44f3
Revises: fc9e2ca8054f
Create Date: 2022-12-04 23:54:12.055635

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0efdfdec44f3'
down_revision = 'fc9e2ca8054f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('address', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('address1', sa.String(), nullable=False),
                    sa.Column('address2', sa.String(), nullable=True),
                    sa.Column('city', sa.String(), nullable=False),
                    sa.Column('state', sa.String(), nullable=False),
                    sa.Column('country', sa.String(), nullable=False),
                    sa.Column('postal_code', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_table('address')
