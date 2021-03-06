"""empty message

Revision ID: 195ef9e0c1d4
Revises: f45cab02f902
Create Date: 2020-10-03 21:09:10.825354

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '195ef9e0c1d4'
down_revision = 'f45cab02f902'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'documents', 'user', ['requester'], ['username'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'documents', type_='foreignkey')
    # ### end Alembic commands ###
