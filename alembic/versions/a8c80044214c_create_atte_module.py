"""create Atte module

Revision ID: a8c80044214c
Revises: 5c072d026c78
Create Date: 2019-03-07 00:55:40.047913

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8c80044214c'
down_revision = '5c072d026c78'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('attes',
    sa.Column('m_id', sa.Integer(), nullable=False),
    sa.Column('y_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['m_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['y_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('m_id', 'y_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('attes')
    # ### end Alembic commands ###
