"""empty message

Revision ID: c9497a0c7087
Revises: 4f2fdf54efe0
Create Date: 2021-07-05 22:05:57.121372

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9497a0c7087'
down_revision = '4f2fdf54efe0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('documents_ibfk_3_idx', table_name='documents')
    op.create_foreign_key(None, 'documents', 'department', ['destiny'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'documents', type_='foreignkey')
    op.create_index('documents_ibfk_3_idx', 'documents', ['destiny'], unique=False)
    # ### end Alembic commands ###