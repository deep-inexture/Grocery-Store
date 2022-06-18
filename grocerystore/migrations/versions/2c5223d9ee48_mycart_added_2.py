"""MyCart Added-2

Revision ID: 2c5223d9ee48
Revises: 9d41849d30bf
Create Date: 2022-06-17 17:35:45.027001

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c5223d9ee48'
down_revision = '9d41849d30bf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('my_cart', sa.Column('status', sa.String(length=10), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('my_cart', 'status')
    # ### end Alembic commands ###