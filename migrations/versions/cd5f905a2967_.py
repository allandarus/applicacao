"""empty message

Revision ID: cd5f905a2967
Revises: 8abf4a4cb8ca
Create Date: 2020-10-03 19:48:06.398535

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd5f905a2967'
down_revision = '8abf4a4cb8ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'documents', 'cargo', ['requester'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'documents', type_='foreignkey')
    # ### end Alembic commands ###
