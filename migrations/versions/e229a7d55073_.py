"""empty message

Revision ID: e229a7d55073
Revises: a26016b00310
Create Date: 2020-10-03 19:51:56.475250

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e229a7d55073'
down_revision = 'a26016b00310'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('documents_ibfk_2', 'documents', type_='foreignkey')
    op.create_foreign_key(None, 'documents', 'user', ['requester'], ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'documents', type_='foreignkey')
    op.create_foreign_key('documents_ibfk_2', 'documents', 'cargo', ['requester'], ['name'])
    # ### end Alembic commands ###