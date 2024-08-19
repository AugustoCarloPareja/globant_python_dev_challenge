# -*- coding: utf-8 -*-
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from app.cache.cache_handler import RedisCacheHandler

client = TestClient(app)
mock_cache = MagicMock(spec=RedisCacheHandler)

def test_all_berry_stats():
    """
    Test the '/allBerryStats' endpoint for a valid response.
    
    This test mocks the `get_berry_stats` function to return a predefined set of
    berry statistics, and verifies that the correct values are returned by the API.
    
    It also checks for the presence of keys like 'berries_names', 'min_growth_time',
    'median_growth_time', 'max_growth_time', 'variance_growth_time', 'mean_growth_time', 
    and 'frequency_growth_time' in the response, and asserts the values are as expected.
    """
    with patch('app.cache.cache_handler.RedisCacheHandler', return_value=mock_cache):
        mock_cache.clear()

    with patch('app.controllers.berry_controller.get_berry_stats', return_value={
        "berries_names": ["cheri", "pecha"],
        "min_growth_time": 3,
        "median_growth_time": 4.0,
        "max_growth_time": 7,
        "variance_growth_time": 2.0,
        "mean_growth_time": 5.0,
        "frequency_growth_time": {"3": 1, "7": 1}
    }):
        response = client.get("/allBerryStats")
        assert response.status_code == 200
        data = response.json()
        
        assert "berries_names" in data
        assert data["berries_names"] == ["cheri", "pecha"]
        
        assert "min_growth_time" in data
        assert data["min_growth_time"] == 3
        
        assert "median_growth_time" in data
        assert data["median_growth_time"] == 4.0
        
        assert "max_growth_time" in data
        assert data["max_growth_time"] == 7
        
        assert "variance_growth_time" in data
        assert data["variance_growth_time"] == 2.0
        
        assert "mean_growth_time" in data
        assert data["mean_growth_time"] == 5.0
        
        assert "frequency_growth_time" in data
        assert data["frequency_growth_time"] == {"3": 1, "7": 1}

def test_all_berry_stats_empty():
    """
    Test the '/allBerryStats' endpoint when no berry data is available.

    This test mocks the `get_berry_stats` function to return an empty dataset and
    verifies that the API responds with no berry data, and 'min_growth_time', 'max_growth_time',
    and 'mean_growth_time' are set to `None`.
    """
    with patch('app.cache.cache_handler.RedisCacheHandler', return_value=mock_cache):
        mock_cache.clear()
        
    with patch('app.controllers.berry_controller.get_berry_stats', return_value={
        "berries_names": [],
        "min_growth_time": None,
        "max_growth_time": None,
        "mean_growth_time": None,
        "variance_growth_time": None,
        "frequency_growth_time": {}
    }):
        response = client.get("/allBerryStats")
        assert response.status_code == 200
        data = response.json()
        assert data["berries_names"] == []
        assert data["min_growth_time"] is None
        assert data["max_growth_time"] is None
        assert data["mean_growth_time"] is None

def test_invalid_url():
    """
    Test that the API correctly returns a 404 error for an invalid endpoint.

    This test sends a GET request to an invalid endpoint (`/invalidEndpoint`) 
    and verifies that the API returns a 404 status code.
    """
    response = client.get("/invalidEndpoint")
    assert response.status_code == 404