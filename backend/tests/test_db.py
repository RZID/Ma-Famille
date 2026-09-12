from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app


def _sqlite_session_factory():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return TestingSession


def test_base_metadata_exists():
    assert hasattr(Base, "metadata")


def test_health_db_ok_with_override():
    from fastapi.testclient import TestClient

    TestingSession = _sqlite_session_factory()

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        client = TestClient(app)
        res = client.get("/api/v1/health/db")
        assert res.status_code == 200
        assert res.json() == {"status": "ok", "database": "reachable"}
    finally:
        app.dependency_overrides.pop(get_db, None)


def test_health_db_503_when_unreachable():
    from fastapi.testclient import TestClient

    def override_get_db_broken():
        raise RuntimeError("boom")
        yield None

    app.dependency_overrides[get_db] = override_get_db_broken
    try:
        client = TestClient(app)
        res = client.get("/api/v1/health/db")
        assert res.status_code in (500, 503)
    finally:
        app.dependency_overrides.pop(get_db, None)
