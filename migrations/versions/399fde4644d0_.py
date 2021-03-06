"""empty message

Revision ID: 399fde4644d0
Revises: 11925c05c683
Create Date: 2020-10-02 19:58:24.809474

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '399fde4644d0'
down_revision = '11925c05c683'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('department', sa.String(length=40), nullable=False))
    op.drop_column('user', 'setor')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('setor', mysql.VARCHAR(collation='utf8mb4_general_ci', length=40), nullable=False))
    op.drop_column('user', 'department')
    # ### end Alembic commands ###
