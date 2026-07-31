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
    # id is already unique because it's the primary key - no extra
    # unique constraint needed for that rule.
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
    # Drop child table first (it has a foreign key into generation_jobs)
    op.drop_index("ix_image_assets_job_id", table_name="image_assets")
    op.drop_table("image_assets")

    op.drop_index("ix_generation_jobs_status", table_name="generation_jobs")
    op.drop_index("ix_generation_jobs_user_id", table_name="generation_jobs")
    op.drop_table("generation_jobs")

    # Postgres keeps the enum type around after the table is dropped -
    # drop it explicitly or the next migration that recreates it will fail.
    # Harmless no-op on SQLite.
    sa.Enum(name="generationstatus").drop(op.get_bind(), checkfirst=True)