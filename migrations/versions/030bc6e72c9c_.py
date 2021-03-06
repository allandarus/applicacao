"""empty message

Revision ID: 030bc6e72c9c
Revises: f40b983a38d9
Create Date: 2021-07-06 09:26:34.525981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '030bc6e72c9c'
down_revision = 'f40b983a38d9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('num_reg', table_name='documents')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('num_reg', 'documents', ['num_reg'], unique=True)
    # ### end Alembic commands ###
