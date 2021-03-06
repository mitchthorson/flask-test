"""empty message

Revision ID: 19c0c5d509bb
Revises: None
Create Date: 2015-02-14 21:41:18.123651

"""

# revision identifiers, used by Alembic.
revision = '19c0c5d509bb'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('entries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('entries_all', postgresql.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('entries')
    ### end Alembic commands ###
