"""empty message

Revision ID: d02a4d3f585c
Revises: 8ac67e28bee2
Create Date: 2020-10-03 19:30:37.660908

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd02a4d3f585c'
down_revision = '8ac67e28bee2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'documents', 'user', ['requester'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'documents', type_='foreignkey')
    # ### end Alembic commands ###
