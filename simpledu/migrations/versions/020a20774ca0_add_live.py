"""add live

Revision ID: 020a20774ca0
Revises: 2a7ce4bb5b2e
Create Date: 2019-10-01 15:50:26.989461

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '020a20774ca0'
down_revision = '2a7ce4bb5b2e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('live',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('livename', sa.String(length=128), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('user_name', sa.String(length=32), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_name'], ['user.username'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('livename')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('live')
    # ### end Alembic commands ###
