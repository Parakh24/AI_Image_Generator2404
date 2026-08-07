"""create generation_jobs and image_assets tables

Revision ID: 0001
Revises:
Create Date: 2026-07-30

"""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Create the generation-jobs and image-assets tables and their indexes."""
    op.create_table(
        "generation_jobs",
        sa.Column("id", sa.String(length=50), primary_key=True),
        sa.Column("user_id", sa.String(length=50), nullable=False),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column(
            "aspect_ratio", sa.String(length=10), nullable=False, server_default="1:1"
        ),
        sa.Column(
            "status",
            sa.Enum("PENDING", "PROCESSING", "COMPLETED", "FAILED", name="generationstatus"),
            nullable=False,
            server_default="PENDING",
        ),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )
    
    # Indexes for fast filtering
    op.create_index("ix_generation_jobs_user_id", "generation_jobs", ["user_id"])
    op.create_index("ix_generation_jobs_status", "generation_jobs", ["status"])

    op.create_table(
        "image_assets",
        sa.Column("id", sa.String(length=50), primary_key=True),
        sa.Column(
            "job_id",
            sa.String(length=50),
            sa.ForeignKey("generation_jobs.id"),
            nullable=False,
        ),
        sa.Column("image_url", sa.String(length=500), nullable=False),
        sa.Column("width", sa.Integer(), nullable=True),
        sa.Column("height", sa.Integer(), nullable=True),
        sa.Column("seed", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_image_assets_job_id", "image_assets", ["job_id"])


def downgrade():
    """Remove the image-assets and generation-jobs schema created above."""
    # Drop child table first
    op.drop_index("ix_image_assets_job_id", table_name="image_assets")
    op.drop_table("image_assets")

    # Drop generation_jobs table & indexes
    op.drop_index("ix_generation_jobs_status", table_name="generation_jobs")
    op.drop_index("ix_generation_jobs_user_id", table_name="generation_jobs")
    op.drop_table("generation_jobs")

    # Drop Postgres Enum explicitly
    sa.Enum(name="generationstatus").drop(op.get_bind(), checkfirst=True)
