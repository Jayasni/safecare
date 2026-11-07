import os

TEST_DATABASE_NAME = "sagecare_db_test"
TEST_DATABASE_URL = f"postgresql://postgres:12345@localhost:5432/{TEST_DATABASE_NAME}"

os.environ.setdefault("DATABASE_URL", TEST_DATABASE_URL)
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("APP_ENV", "testing")
os.environ.setdefault("DEBUG", "False")
os.environ.setdefault("FRONTEND_URL", "http://localhost:5173")

from sqlalchemy import create_engine, text

admin_engine = create_engine(
    "postgresql://postgres:12345@localhost:5432/postgres",
    isolation_level="AUTOCOMMIT",
)
with admin_engine.connect() as connection:
    exists = connection.execute(
        text("SELECT 1 FROM pg_database WHERE datname = :name"),
        {"name": TEST_DATABASE_NAME},
    ).scalar()
    if not exists:
        connection.execute(text(f'CREATE DATABASE "{TEST_DATABASE_NAME}"'))

from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.main import app

Base.metadata.create_all(bind=engine)

from fastapi.testclient import TestClient
import pytest


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture()
def admin_user(client):
    from app.core.security import hash_password
    from app.models.enums import UserRole
    from app.models.user import User

    db = SessionLocal()
    user = User(
        full_name="Test Admin",
        email="admin@test.com",
        password_hash=hash_password("AdminPass123"),
        role=UserRole.admin,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.close()
    return user