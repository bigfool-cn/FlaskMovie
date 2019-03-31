"""empty message

Revision ID: e29609b6ef28
Revises: eff3b5f110a0
Create Date: 2018-01-10 22:20:36.136267

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'e29609b6ef28'
down_revision = 'eff3b5f110a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('moviecols',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('addtime', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_moviecols_addtime'), 'moviecols', ['addtime'], unique=False)
    op.drop_table('movicecols')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('movicecols',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('movie_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('addtime', mysql.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.id'], name='movicecols_ibfk_1'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='movicecols_ibfk_2'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.drop_index(op.f('ix_moviecols_addtime'), table_name='moviecols')
    op.drop_table('moviecols')
    # ### end Alembic commands ###