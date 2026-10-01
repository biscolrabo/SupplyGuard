import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# Settings require DATABASE_URL; provide a dummy one so tests never touch the main database.
os.environ.setdefault("DATABASE_URL", "postgresql+psycopg://test:test@localhost:5432/test")

from app.core.config import settings  # noqa: E402
from app.core.database import get_db  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(scope="session")
def test_engine():
    if not settings.test_database_url:
        pytest.skip("TEST_DATABASE_URL is not set")
    engine = create_engine(settings.test_database_url, pool_pre_ping=True)
    yield engine
    engine.dispose()


@pytest.fixture
def db_session(test_engine) -> Generator[Session]:
    # Todo el test va dentro de una transacción que se deshace al final:
    # los commit() del código solo cierran un savepoint, así la BD de test queda limpia
    connection = test_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection, join_transaction_mode="create_savepoint")
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient]:
    app.dependency_overrides[get_db] = lambda: db_session
    yield TestClient(app)
    app.dependency_overrides.clear()
