import pytest
from fastapi.testclient import TestClient

from madr_postgres.app import app


@pytest.fixture
def client():
    client = TestClient(app)
    return client
