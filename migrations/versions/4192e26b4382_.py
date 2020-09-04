"""empty message

Revision ID: 4192e26b4382
Revises: 5899d30a0c54
Create Date: 2020-09-02 08:17:26.880769

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4192e26b4382'
down_revision = '5899d30a0c54'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('genres', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'genres')
    # ### end Alembic commands ###
