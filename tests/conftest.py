import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    # Import here to avoid circular imports and allow env var setup
    from main import app

    with TestClient(app) as test_client:
        yield test_client
