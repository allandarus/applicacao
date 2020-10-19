"""empty message

Revision ID: da947b45c7d3
Revises: d02a4d3f585c
Create Date: 2020-10-03 19:31:11.844351

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da947b45c7d3'
down_revision = 'd02a4d3f585c'
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