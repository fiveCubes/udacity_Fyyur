"""empty message

Revision ID: cb4db9fd0ab1
Revises: 84084dd1c091
Create Date: 2020-09-02 15:40:17.052643

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb4db9fd0ab1'
down_revision = '84084dd1c091'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Venue')
    op.drop_table('Artist')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Artist',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Artist_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('city', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('state', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('phone', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('genres', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('image_link', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('website_link', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('Seeking_Venue', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('Seeking_description', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('facebook_link', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='Artist_pkey')
    )
    op.create_table('Venue',
    sa.Column('id', sa.INTEGER(), server_default=sa.text('nextval(\'"Venue_id_seq"\'::regclass)'), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('city', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('state', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('address', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('phone', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('image_link', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('website_link', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('Seeking_Talent', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('Seeking_description', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('facebook_link', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.Column('genres', sa.VARCHAR(length=120), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='Venue_pkey')
    )
    # ### end Alembic commands ###
