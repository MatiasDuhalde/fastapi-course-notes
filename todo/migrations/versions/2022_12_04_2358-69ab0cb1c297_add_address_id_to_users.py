"""add address_id to users

Revision ID: 69ab0cb1c297
Revises: 0efdfdec44f3
Create Date: 2022-12-04 23:58:04.689607

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '69ab0cb1c297'
down_revision = '0efdfdec44f3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('address_id', sa.Integer(), nullable=True))
    op.create_foreign_key('users_address_id_fkey',
                          'users',
                          'address', ['address_id'], ['id'],
                          ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('users_address_id_fkey', 'users', type_='foreignkey')
    op.drop_column('users', 'address_id')
