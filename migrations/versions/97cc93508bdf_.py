"""empty message

Revision ID: 97cc93508bdf
Revises: 34d46fd4354b
Create Date: 2021-07-06 10:35:13.559653

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97cc93508bdf'
down_revision = '34d46fd4354b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'documents', 'department', ['destiny'], ['id'])
    op.create_foreign_key(None, 'documents', 'types_reg', ['type'], ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'documents', type_='foreignkey')
    op.drop_constraint(None, 'documents', type_='foreignkey')
    # ### end Alembic commands ###
