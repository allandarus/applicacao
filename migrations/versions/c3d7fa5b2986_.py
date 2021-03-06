"""empty message

Revision ID: c3d7fa5b2986
Revises: 77813524fea3
Create Date: 2020-10-02 17:36:04.582460

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3d7fa5b2986'
down_revision = '77813524fea3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cargo', sa.Column('description', sa.String(length=60), nullable=True))
    op.add_column('types_reg', sa.Column('description', sa.String(length=60), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('types_reg', 'description')
    op.drop_column('cargo', 'description')
    # ### end Alembic commands ###
