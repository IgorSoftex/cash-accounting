"""migration 11

Revision ID: 7b669cb2a468
Revises: b26a2b40d10e
Create Date: 2023-03-13 17:33:43.130230

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '7b669cb2a468'
down_revision = 'b26a2b40d10e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('clients', schema=None) as batch_op:
        batch_op.drop_column('edrpou_code')
        batch_op.drop_column('address')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('clients', schema=None) as batch_op:
        batch_op.add_column(sa.Column('address', mysql.VARCHAR(collation='utf8mb4_0900_as_ci', length=200), nullable=False))
        batch_op.add_column(sa.Column('edrpou_code', mysql.VARCHAR(collation='utf8mb4_0900_as_ci', length=20), nullable=False))

    # ### end Alembic commands ###
