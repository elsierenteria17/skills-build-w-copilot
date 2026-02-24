import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities as activities_store


_initial_snapshot = copy.deepcopy(activities_store)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Restore a fresh copy of the in-memory activities before each test."""
    activities_store.clear()
    activities_store.update(copy.deepcopy(_initial_snapshot))
    yield