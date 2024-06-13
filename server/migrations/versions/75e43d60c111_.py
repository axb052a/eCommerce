"""empty message

Revision ID: 75e43d60c111
Revises: e15f74a29c25
Create Date: 2024-03-13 21:13:06.284245

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75e43d60c111'
down_revision = 'e15f74a29c25'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(batch_op.f('fk_products_category_id_categories'), 'categories', ['category_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_products_category_id_categories'), type_='foreignkey')
        batch_op.drop_column('category_id')

    op.drop_table('categories')
    # ### end Alembic commands ###
