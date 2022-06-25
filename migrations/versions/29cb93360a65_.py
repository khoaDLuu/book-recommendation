"""empty message

Revision ID: 29cb93360a65
Revises: 33b112d653fa
Create Date: 2022-06-24 22:15:34.239257

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29cb93360a65'
down_revision = '33b112d653fa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bookbuys', sa.Column('book_id', sa.Integer(), nullable=True))
    op.drop_column('bookbuys', 'book_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bookbuys', sa.Column('book_name', sa.VARCHAR(length=4096), autoincrement=False, nullable=True))
    op.drop_column('bookbuys', 'book_id')
    # ### end Alembic commands ###