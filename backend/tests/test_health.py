from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from app.core.database import get_db
from app.main import app

client = TestClient(app)


def override_db(session: MagicMock) -> None:
    """Replace the real database session with a fake one (no Neon in tests)."""
    app.dependency_overrides[get_db] = lambda: session


def teardown_function() -> None:
    app.dependency_overrides.clear()


def test_health_returns_ok_when_database_responds():
    override_db(MagicMock())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}


def test_health_returns_503_when_database_is_down():
    session = MagicMock()
    session.execute.side_effect = OperationalError("SELECT 1", {}, Exception("boom"))
    override_db(session)

    response = client.get("/health")

    assert response.status_code == 503
    assert response.json() == {"detail": "Database unavailable"}
