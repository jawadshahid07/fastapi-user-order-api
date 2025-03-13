from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context

from models import Base

from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Get database URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Import Alembic config
config = context.config

# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import your models' metadata for 'autogenerate' support
# from yourapp.models import Base
target_metadata = Base.metadata  # Change this to `Base.metadata` if you have models

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,  # Use the DATABASE_URL from .env
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    engine = create_engine(DATABASE_URL, poolclass=pool.NullPool)  # Use DATABASE_URL

    with engine.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
