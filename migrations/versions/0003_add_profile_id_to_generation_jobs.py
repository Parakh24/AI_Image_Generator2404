"""add profile_id to generation_jobs

Revision ID: 0003
Revises: 0002
Create Date: 2026-08-06

"""
from alembic import op
import sqlalchemy as sa

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "generation_jobs",
        sa.Column(
            "profile_id",
            sa.String(length=50),
            nullable=False,
            server_default="",
        ),
    )
    with op.batch_alter_table("generation_jobs") as batch_op:
        batch_op.alter_column("profile_id", server_default=None)


def downgrade():
    op.drop_column("generation_jobs", "profile_id")
