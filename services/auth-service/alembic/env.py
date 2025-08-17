# It lets you load logging settings from a config file — in this case, alembic.ini.
from logging.config import fileConfig

# It is used to create a database engine using settings from a config file — typically alembic.ini.
from sqlalchemy import engine_from_config

# Each command (like alembic upgrade head) is short-lived.
# Keeping a connection pool is unnecessary — it just adds overhead.
# So Alembic disables it using this import.
from sqlalchemy import pool

# Think of it like Alembic’s control panel — a Python object that knows:
# Where the migration is running (online/offline)
# What database you're using
# What your models look like
# How to run the migration step-by-step
from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

from app.models.user import Base

# Interpret the config file for Python logging.
# If the config file path exists, this line loads the logging configuration from that file.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# Alembic needs to know the structure of your current models so it can compare them with the actual database schema.
# This comparison helps Alembic generate migration scripts automatically (called autogeneration).
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")

    """
    This method sets up Alembic’s migration context, which controls how migrations behave during a run.
    It tells Alembic important info like:
    How to connect to the database (or just the URL for offline),
    What the schema looks like (target_metadata),
    How to render SQL statements, etc.
    """
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
