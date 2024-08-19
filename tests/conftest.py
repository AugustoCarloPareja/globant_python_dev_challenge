# -*- coding: utf-8 -*-
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """Fixture to create a test client for FastAPI."""
    return TestClient(app)