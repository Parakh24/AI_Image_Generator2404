"""Add tenant isolation to generation jobs.

Revision ID: 0004
Revises: 0003
Create Date: 2026-08-07
"""

from alembic import op
import sqlalchemy as sa


revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade():
    """Add and index the tenant identifier used by generation-job queries."""
    op.add_column(
        "generation_jobs",
        sa.Column(
            "tenant_id",
            sa.String(length=50),
            nullable=False,
            server_default="",
        ),
    )
    with op.batch_alter_table("generation_jobs") as batch_op:
        batch_op.alter_column("tenant_id", server_default=None)
        batch_op.create_index("ix_generation_jobs_tenant_id", ["tenant_id"])


def downgrade():
    """Remove the tenant index and identifier from generation jobs."""
    with op.batch_alter_table("generation_jobs") as batch_op:
        batch_op.drop_index("ix_generation_jobs_tenant_id")
        batch_op.drop_column("tenant_id")
