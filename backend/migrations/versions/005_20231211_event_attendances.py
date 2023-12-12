"""empty message

Revision ID: 8ff56df3e95b
Revises: 005
Create Date: 2023-12-11 19:24:48.118928

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ff56df3e95b'
down_revision = '004'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'event_attendances',
        sa.Column('created', sa.DateTime(), nullable=True),
        sa.Column('updated', sa.DateTime(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column("event_line_id", sa.Integer, sa.ForeignKey("event_lines.id"), nullable=False),
        sa.Column("event_registration_id", sa.Integer, sa.ForeignKey("event_registrations.id"), nullable=False),
        sa.Column('date_claim', sa.DateTime(), nullable=False),
        sa.Column('created_uid', sa.Integer(), nullable=False),
        sa.Column('updated_uid', sa.Integer(), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=True),
        sa.Column('deleted', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('event_attendances')
