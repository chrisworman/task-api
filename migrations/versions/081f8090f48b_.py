"""empty message

Revision ID: 081f8090f48b
Revises: 
Create Date: 2017-10-03 11:38:10.723185

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '081f8090f48b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('list_id', sa.Integer(), nullable=True),
    sa.Column('text', sa.String(length=511), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_modified', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tasks')
    # ### end Alembic commands ###
