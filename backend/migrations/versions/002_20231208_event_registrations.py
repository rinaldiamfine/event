"""Events Registrations model

Revision ID: 002
Revises: 001
Create Date: 2023-12-08 08:12:52.259225

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


registration_type = (
    "AUDIENCE",
    "SPEAKER",
)
enum_registration_type = sa.Enum(
    *registration_type,
    name="registration_type",
)

def upgrade():
    # enum_registration_type.create(op.get_bind(), checkfirst=False)
    op.create_table(
        'event_registrations',
        sa.Column('created', sa.DateTime(), nullable=True),
        sa.Column('updated', sa.DateTime(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', sa.String(), nullable=False),
        sa.Column("event_id", sa.Integer, sa.ForeignKey("events.id"), nullable=False),
        sa.Column('registration_id', sa.String(length=50), nullable=True),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=150), nullable=False), ## Set nullable to false because we need to sent the invitation via email
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('institution', sa.String(length=50), nullable=True),
        sa.Column('on_behalf', sa.String(length=50), nullable=True),
        sa.Column('created_uid', sa.Integer(), nullable=False),
        sa.Column('updated_uid', sa.Integer(), nullable=False),
        sa.Column('is_attendance', sa.Boolean(), nullable=True),
        sa.Column('date_attendance', sa.DateTime(), nullable=True),
        sa.Column('registration_type', enum_registration_type),
        sa.Column('is_deleted', sa.Boolean(), nullable=True),
        sa.Column('deleted', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('event_registrations')
    enum_registration_type.drop(op.get_bind(), checkfirst=False)