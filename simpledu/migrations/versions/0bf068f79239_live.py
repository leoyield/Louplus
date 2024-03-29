"""live

Revision ID: 0bf068f79239
Revises: 020a20774ca0
Create Date: 2019-10-01 15:57:14.860434

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0bf068f79239'
down_revision = '020a20774ca0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('live_ibfk_2', 'live', type_='foreignkey')
    op.drop_column('live', 'user_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('live', sa.Column('user_name', mysql.VARCHAR(length=32), nullable=True))
    op.create_foreign_key('live_ibfk_2', 'live', 'user', ['user_name'], ['username'], ondelete='CASCADE')
    # ### end Alembic commands ###
