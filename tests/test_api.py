from app.cache.cache_handler import cache
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)

def test_all_berry_stats():
    cache.clear()
    
    with patch('app.controllers.berry_controller.get_berry_stats', return_value={
        "berries_names": ["cheri", "pecha"],
        "min_growth_time": 3,
        "median_growth_time": 4.0,
        "max_growth_time": 7,
        "variance_growth_time": 2.0,
        "mean_growth_time": 5.0,
        "frequency_growth_time": {3: 1, 7: 1}
    }):
        response = client.get("/allBerryStats")
        assert response.status_code == 200
        data = response.json()
        assert "berries_names" in data
        assert data["min_growth_time"] == 3
        assert data["median_growth_time"] == 4.0
        assert data["max_growth_time"] == 7

def test_all_berry_stats_empty():
    cache.clear()

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
    response = client.get("/invalidEndpoint")
    assert response.status_code == 404