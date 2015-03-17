"""empty message

Revision ID: 253a5c28b668
Revises: None
Create Date: 2015-03-09 22:11:59.699143

"""

# revision identifiers, used by Alembic.
revision = '253a5c28b668'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('project',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('projectType', sa.String(length=255), nullable=True),
    sa.Column('tags', sa.String(length=255), nullable=True),
    sa.Column('externalLink', sa.String(length=255), nullable=True),
    sa.Column('imagesLinks', sa.String(length=255), nullable=True),
    sa.Column('snippet', sa.String(length=255), nullable=True),
    sa.Column('date', sa.Integer(), nullable=True),
    sa.Column('codeLink', sa.String(length=255), nullable=True),
    sa.Column('cover_photo', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstname', sa.String(length=100), nullable=True),
    sa.Column('lastname', sa.String(length=100), nullable=True),
    sa.Column('login', sa.String(length=80), nullable=True),
    sa.Column('username', sa.String(length=20), nullable=True),
    sa.Column('password', sa.String(length=10), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('registered_on', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('login')
    )
    op.create_index(u'ix_user_email', 'user', ['email'], unique=True)
    op.create_index(u'ix_user_username', 'user', ['username'], unique=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(u'ix_user_username', table_name='user')
    op.drop_index(u'ix_user_email', table_name='user')
    op.drop_table('user')
    op.drop_table('project')
    ### end Alembic commands ###
