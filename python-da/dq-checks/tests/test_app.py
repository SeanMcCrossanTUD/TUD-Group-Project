import pytest
import sys
import os
sys.path.append(os.path.abspath('src'))
from app import app
#from src.app import app

@pytest.fixture
def client():
    """
    Setup Flask test client before running a test.
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """
    Test the health check endpoint.
    """
    # Make a GET request to the health check endpoint
    response = client.get('/health')
    
    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200, f"Expected status code 200 but got {response.status_code}"
    
    # Assert that the response data is as expected
    expected_data = {
        "status": "healthy",
        "version": "1.0.0"
    }
    assert response.get_json() == expected_data, f"Expected response data {expected_data} but got {response.get_json()}"

