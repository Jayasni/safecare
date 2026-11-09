
from logging.config import fileConfig

from sqlalchemy import create_engine, pool

from alembic import context

from app.database import Base
from app.core.config import settings

# Import all models so SQLAlchemy registers their tables.
from app.models import (
    User,
    Doctor,
    Patient,
    Appointment,
     Hospital,
    MedicalService,
    DoctorHospital,
    DoctorAvailability,
    DoctorHospitalService,
)

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Connect Alembic to Healora's SQLAlchemy metadata.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations without creating a database connection."""

    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations using a live database connection."""

    connectable = create_engine(
        settings.DATABASE_URL,
        poolclass=pool.NullPool,
        pool_pre_ping=True,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

    connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
