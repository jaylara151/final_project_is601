from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


# This creates a fake SQLite database just for testing.
# It does not create a real file, so it avoids permission problems.
TEST_DATABASE_URL = "sqlite://"


test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def get_test_client():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    client = TestClient(app)

    return client


import pytest


@pytest.fixture()
def client():
    test_client = get_test_client()

    yield test_client

    Base.metadata.drop_all(bind=test_engine)