import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def original_activities():
    """Store original activities state"""
    return deepcopy(activities)


@pytest.fixture(autouse=True)
def reset_activities(original_activities):
    """Reset activities to original state before each test
    
    This fixture ensures test isolation by restoring the in-memory
    activity database to its initial state before and after each test.
    """
    activities.clear()
    activities.update(deepcopy(original_activities))
    yield
    # Cleanup after test
    activities.clear()
    activities.update(deepcopy(original_activities))


@pytest.fixture
def client():
    """Provide TestClient for making HTTP requests to the FastAPI app"""
    return TestClient(app)
