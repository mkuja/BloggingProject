"""Initial tables setup

Revision ID: 76810ae89689
Revises: 
Create Date: 2022-07-17 19:33:30.469789

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76810ae89689'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_account',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=25), nullable=False),
    sa.Column('username', sa.String(length=25), nullable=False),
    sa.Column('email', sa.String(length=40), nullable=False),
    sa.Column('password_hash', sa.String(length=120), nullable=False),
    sa.Column('is_author', sa.Boolean(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('registration_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('blog_post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('published', sa.DateTime(), nullable=False),
    sa.Column('summary', sa.Text(), nullable=True),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user_account.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nickname', sa.String(length=20), nullable=True),
    sa.Column('comment', sa.Text(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['comment.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user_account.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(), nullable=False),
    sa.Column('absolute_path', sa.String(), nullable=False),
    sa.Column('caption', sa.String(), nullable=True),
    sa.Column('blog_post_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['blog_post_id'], ['blog_post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('images')
    op.drop_table('comment')
    op.drop_table('blog_post')
    op.drop_table('user_account')
    # ### end Alembic commands ###
