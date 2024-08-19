import pytest
from app.services.berry_service import get_berry_stats
from app.cache.cache_handler import cache
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
async def test_get_berry_stats_valid_data():
    cache.clear()
    
    mock_berries = [
        {'name': 'cheri', 'growth_time': 3},
        {'name': 'pecha', 'growth_time': 5},
        {'name': 'oran', 'growth_time': 7},
    ]
    
    with patch('app.services.berry_service.fetch_all_berries', new=AsyncMock(return_value=mock_berries)) as mock_fetch:
        stats = await get_berry_stats()
        
        mock_fetch.assert_called_once()
    
    assert stats["berries_names"] == ["cheri", "pecha", "oran"]
    assert stats["min_growth_time"] == 3
    assert stats["median_growth_time"] == 5
    assert stats["max_growth_time"] == 7

@pytest.mark.asyncio
async def test_get_berry_stats_no_data():
    cache.clear()
    
    mock_berries = []
    with patch('app.services.berry_service.fetch_all_berries', new=AsyncMock(return_value=mock_berries)) as mock_fetch:
        stats = await get_berry_stats()
        
        mock_fetch.assert_called_once()
    
    assert stats["berries_names"] == []
    assert stats["min_growth_time"] is None
    assert stats["max_growth_time"] is None
    assert stats["mean_growth_time"] is None
    assert stats["variance_growth_time"] is None
    assert stats["frequency_growth_time"] == {}

@pytest.mark.asyncio
async def test_get_berry_stats_with_cache():
    cached_stats = {
        "berries_names": ["cached_cheri"],
        "min_growth_time": 1,
        "max_growth_time": 1,
        "mean_growth_time": 1.0,
        "variance_growth_time": 0.0,
        "frequency_growth_time": {1: 1}
    }
    cache['berry_stats'] = cached_stats
    
    stats = await get_berry_stats()
    assert stats == cached_stats