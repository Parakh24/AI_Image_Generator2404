"""
env.py

Alembic's runtime configuration file. Its responsibilities are:

1. Import the project's `app.database.Base` (which contains all
   registered SQLAlchemy models via `Base.metadata`) so Alembic knows
   what the expected database schema should look like.
2. Configure the database connection URL.
3. Run migrations either in:
   - Offline mode (generate SQL scripts without connecting to the database), or
   - Online mode (apply migrations directly to the database).

You normally do not need to modify this file. Once it is set up,
every new migration will reuse this configuration.
"""

import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# Add the project root to the Python path so the "app" package
# can be imported successfully.
sys.path.insert(0, os.getcwd())

from app.database import Base

# Every model must be imported here. Otherwise, Base.metadata
# will not be aware of tables such as generation_jobs or
# image_assets, causing Alembic's autogenerate feature to
# produce an empty migration.
from app.feature.image_generation.models.generation_job import GenerationJob  # noqa: F401
from app.feature.image_generation.models.image_asset import ImageAsset  # noqa: F401

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# The expected database schema that Alembic compares
# against the actual database schema.
target_metadata = Base.metadata


def get_url() -> str:
    """
    Use the DATABASE_URL environment variable if it is available
    (recommended for production and staging environments).
    Otherwise, fall back to the default URL defined in alembic.ini.
    """
    return os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url"))


def run_migrations_offline():
    """
    Generate SQL migration scripts without establishing
    a connection to the database.
    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """
    Connect to the database and apply migrations directly.
    """
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()