"""empty message

Revision ID: a736e01fa9e9
Revises: 7e9deb15d5ef
Create Date: 2024-04-25 19:25:47.097381

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a736e01fa9e9'
down_revision = '7e9deb15d5ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('currency_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('climate_type', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=100), nullable=False))

    with op.batch_alter_table('industry_type', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=100), nullable=False))

    with op.batch_alter_table('language_type', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=100), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('language_type', schema=None) as batch_op:
        batch_op.drop_column('name')

    with op.batch_alter_table('industry_type', schema=None) as batch_op:
        batch_op.drop_column('name')

    with op.batch_alter_table('climate_type', schema=None) as batch_op:
        batch_op.drop_column('name')

    op.drop_table('currency_type')
    # ### end Alembic commands ###
