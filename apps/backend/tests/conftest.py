"""Shared test fixtures for gimnasio backend tests.

Uses in-memory SQLite for isolation and httpx TestClient for integration tests.
"""

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

# Ensure src is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.core.database import Base, get_db
from src.core.security import create_access_token
from src.main import app
from src.models.db import Exercise, User


# ---------------------------------------------------------------------------
# Database fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="function")
def db_session():
    """Create an in-memory SQLite session for each test."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestSession = sessionmaker(bind=engine)

    session = TestSession()
    yield session
    session.close()


@pytest.fixture(scope="function")
def client(db_session):
    """FastAPI TestClient with overridden DB dependency."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session) -> User:
    """Create a test user in the database."""
    user = User(
        email="test@example.com",
        password_hash="hashed_password_placeholder",
        display_name="Test User",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_headers(test_user) -> dict:
    """Generate JWT auth headers for the test user."""
    token = create_access_token(test_user.id)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def seed_exercises(db_session, test_user) -> list[Exercise]:
    """Seed a few exercises for testing."""
    exercises = [
        Exercise(name="Bench Press", category="strength", muscle_groups='["chest","triceps"]', equipment="barbell"),
        Exercise(name="Squat", category="strength", muscle_groups='["quads","glutes"]', equipment="barbell"),
        Exercise(name="Treadmill", category="cardio", muscle_groups='["cardio"]', equipment="treadmill"),
    ]
    db_session.add_all(exercises)
    db_session.commit()
    for e in exercises:
        db_session.refresh(e)
    return exercises
