import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app


def get_client() -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def _isolate_secrets():
    """Tests must not depend on ambient .env secrets (keys, tokens).

    Individual tests opt back in via monkeypatch. Note: route prefixes are
    baked at import time, so API_V1_PREFIX/ROOT_PATH always come from the
    ambient env — keep them at defaults when running tests.
    """
    old = (settings.doku_client_id, settings.doku_secret_key, settings.manager_token)
    settings.doku_client_id = ""
    settings.doku_secret_key = ""
    settings.manager_token = ""
    yield
    settings.doku_client_id, settings.doku_secret_key, settings.manager_token = old
