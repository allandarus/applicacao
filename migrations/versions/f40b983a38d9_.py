"""empty message

Revision ID: f40b983a38d9
Revises: c9497a0c7087
Create Date: 2021-07-05 22:24:16.193734

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f40b983a38d9'
down_revision = 'c9497a0c7087'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('documents', 'destiny',
               existing_type=mysql.INTEGER(),
               nullable=True)
    op.create_foreign_key(None, 'documents', 'department', ['destiny'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'documents', type_='foreignkey')
    op.alter_column('documents', 'destiny',
               existing_type=mysql.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###