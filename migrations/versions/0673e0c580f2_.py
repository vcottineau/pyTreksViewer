"""empty message

Revision ID: 0673e0c580f2
Revises: c6c717f3952a
Create Date: 2021-12-30 15:20:39.083489

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0673e0c580f2'
down_revision = 'c6c717f3952a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'marker', 'folder', ['folder_id'], ['id'])
    op.create_foreign_key(None, 'marker', 'country', ['country_id'], ['id'])
    op.drop_column('marker', 'country')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('marker', sa.Column('country', sa.VARCHAR(length=128), nullable=True))
    op.drop_constraint(None, 'marker', type_='foreignkey')
    op.drop_constraint(None, 'marker', type_='foreignkey')
    # ### end Alembic commands ###
