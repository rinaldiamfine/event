"""Events and Event Lines model

Revision ID: 001
Revises: 
Create Date: 2023-12-07 08:15:58.280148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'events',
        sa.Column('created', sa.DateTime(), nullable=True),
        sa.Column('updated', sa.DateTime(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('sequence', sa.Integer()),
        sa.Column('event_date', sa.DateTime()),
        sa.Column('event_time', sa.String(length=50)),
        sa.Column('venue', sa.String(length=50)),
        sa.Column('created_uid', sa.Integer(), nullable=False),
        sa.Column('updated_uid', sa.Integer(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=True),
        sa.Column('deleted', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'event_lines',
        sa.Column('created', sa.DateTime(), nullable=True),
        sa.Column('updated', sa.DateTime(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column("event_id", sa.Integer, sa.ForeignKey("events.id"), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('souvenir_cupons', sa.Integer, nullable=True),
        sa.Column('created_uid', sa.Integer(), nullable=False),
        sa.Column('updated_uid', sa.Integer(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=True),
        sa.Column('deleted', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('event_lines')
    op.drop_table('events')
