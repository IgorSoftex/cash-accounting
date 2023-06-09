"""migration 14

Revision ID: 2712e7f0800c
Revises: aaf9df49f48d
Create Date: 2023-03-16 18:37:13.208183

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2712e7f0800c'
down_revision = 'aaf9df49f48d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cash_expenses', schema=None) as batch_op:
        batch_op.alter_column('client_id',
               existing_type=mysql.INTEGER(),
               nullable=False)

    with op.batch_alter_table('cash_receipts', schema=None) as batch_op:
        batch_op.alter_column('client_id',
               existing_type=mysql.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cash_receipts', schema=None) as batch_op:
        batch_op.alter_column('client_id',
               existing_type=mysql.INTEGER(),
               nullable=True)

    with op.batch_alter_table('cash_expenses', schema=None) as batch_op:
        batch_op.alter_column('client_id',
               existing_type=mysql.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###
