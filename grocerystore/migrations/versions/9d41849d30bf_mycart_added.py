"""MyCart Added

Revision ID: 9d41849d30bf
Revises: e0ad265d016e
Create Date: 2022-06-17 13:01:41.440447

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d41849d30bf'
down_revision = 'e0ad265d016e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('my_cart',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('product_name', sa.String(length=255), nullable=False),
    sa.Column('product_quantity', sa.Integer(), nullable=False),
    sa.Column('product_price', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_my_cart_id'), 'my_cart', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_my_cart_id'), table_name='my_cart')
    op.drop_table('my_cart')
    # ### end Alembic commands ###
