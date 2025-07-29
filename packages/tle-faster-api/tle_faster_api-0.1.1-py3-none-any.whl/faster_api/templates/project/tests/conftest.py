import os
import sys

# Add 'backend' directory to sys.path so 'app' package is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'  # for Pydantic Settings

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.db import session as session_module
from app.core.db.base import Base
from app.core.deps import get_db
from app.main import app
from fastapi.testclient import TestClient
from app.auth.crud import create_user
from app.auth.schemas import UserCreate

# SQLite in-memory database URL for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Create test engine and sessionmaker
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the session module's engine and SessionLocal for testing
session_module.engine = engine
session_module.SessionLocal = TestingSessionLocal

@pytest.fixture(scope="function", autouse=True)
def setup_test_database():
    # Create all tables before each test
    Base.metadata.create_all(bind=engine)
    yield
    # Drop all tables after each test to isolate tests
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Return a SQLAlchemy session for a test."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def client(db_session):
    """Return a FastAPI TestClient using the test database session."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def new_user_data():
    """Default data for creating a new user."""
    return {"email": "test@example.com", "password": "password123", "name": "Test User"}

@pytest.fixture(scope="function")
def test_user(db_session, new_user_data):
    """Create and return a test user."""
    user_in = UserCreate(**new_user_data)
    return create_user(db_session, user_in)