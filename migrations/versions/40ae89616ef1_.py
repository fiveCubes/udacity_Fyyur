"""empty message

Revision ID: 40ae89616ef1
Revises: c655ab59d3ba
Create Date: 2020-09-02 15:44:38.877130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40ae89616ef1'
down_revision = 'c655ab59d3ba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('seeking_description', sa.String(length=500), nullable=True))
    op.add_column('Artist', sa.Column('seeking_venue', sa.String(length=120), nullable=True))
    op.drop_column('Artist', 'Seeking_description')
    op.drop_column('Artist', 'Seeking_Venue')
    op.add_column('Venue', sa.Column('seeking_description', sa.String(length=500), nullable=True))
    op.add_column('Venue', sa.Column('seeking_talent', sa.String(length=120), nullable=True))
    op.drop_column('Venue', 'Seeking_description')
    op.drop_column('Venue', 'Seeking_Talent')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('Seeking_Talent', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('Venue', sa.Column('Seeking_description', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    op.drop_column('Venue', 'seeking_talent')
    op.drop_column('Venue', 'seeking_description')
    op.add_column('Artist', sa.Column('Seeking_Venue', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('Artist', sa.Column('Seeking_description', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    op.drop_column('Artist', 'seeking_venue')
    op.drop_column('Artist', 'seeking_description')
    # ### end Alembic commands ###
