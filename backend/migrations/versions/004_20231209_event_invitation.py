"""Event Invitation

Revision ID: 004
Revises: 003
Create Date: 2023-12-09 11:16:22.102721

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'event_invitations',
        sa.Column('created', sa.DateTime(), nullable=True),
        sa.Column('updated', sa.DateTime(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column("event_id", sa.Integer, sa.ForeignKey("events.id"), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=150), nullable=False), ## Set nullable to false because we need to sent the invitation via email
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('on_behalf', sa.String(length=50), nullable=True),
        sa.Column('created_uid', sa.Integer(), nullable=False),
        sa.Column('updated_uid', sa.Integer(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=True),
        sa.Column('deleted', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('event_invitations')
