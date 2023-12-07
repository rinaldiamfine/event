"""Event registration model

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
        'event',
        sa.Column('created', sa.DateTime(), nullable=True),
        sa.Column('updated', sa.DateTime(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=True),
        sa.Column('deleted', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'event_registration',
        sa.Column('created', sa.DateTime(), nullable=True),
        sa.Column('updated', sa.DateTime(), nullable=True),
        sa.Column("event_id", sa.Integer, sa.ForeignKey("event.id"), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('reg_no', sa.String(length=50)),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=150), nullable=True),
        sa.Column('phone', sa.String(length=20), nullable=True),

        sa.Column('is_on_behalf', sa.Boolean(), nullable=True),
        sa.Column('on_behalf', sa.String(length=50), nullable=False),
        
        sa.Column('is_deleted', sa.Boolean(), nullable=True),
        sa.Column('deleted', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('event_registration')
    op.drop_table('event')
