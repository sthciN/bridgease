"""empty message

Revision ID: db5372e37dd2
Revises: 8500da5c5d5d
Create Date: 2024-04-29 01:27:37.488396

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db5372e37dd2'
down_revision = '8500da5c5d5d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('client_visa_programs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('users_id', sa.Integer(), nullable=False),
    sa.Column('visa_programs', sa.JSON(), nullable=True),
    sa.Column('is_latest', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['users_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('client_visa_programs')
    # ### end Alembic commands ###
