"""Create user for authentication

Revision ID: 006
Revises: 005
Create Date: 2023-12-15 20:02:40.159481

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '006'
down_revision = '005'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'commite',
        sa.Column('created', sa.DateTime(), nullable=True),
        sa.Column('updated', sa.DateTime(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('created_uid', sa.Integer(), nullable=False),
        sa.Column('updated_uid', sa.Integer(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=True),
        sa.Column('deleted', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('commite')
