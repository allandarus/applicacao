"""empty message

Revision ID: a26016b00310
Revises: cd5f905a2967
Create Date: 2020-10-03 19:50:16.039934

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a26016b00310'
down_revision = 'cd5f905a2967'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'documents', 'cargo', ['requester'], ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'documents', type_='foreignkey')
    # ### end Alembic commands ###
