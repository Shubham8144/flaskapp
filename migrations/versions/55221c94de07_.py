"""empty message

Revision ID: 55221c94de07
Revises: 61499804ecf9
Create Date: 2022-05-31 12:14:21.189450

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55221c94de07'
down_revision = '61499804ecf9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_config',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('widget_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['widget_id'], ['widget.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_config')
    # ### end Alembic commands ###
