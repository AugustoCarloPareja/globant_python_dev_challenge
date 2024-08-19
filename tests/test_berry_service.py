# -*- coding: utf-8 -*-
import pytest
from unittest.mock import patch, AsyncMock
from app.services.berry_service import get_berry_stats

@pytest.mark.asyncio
async def test_get_berry_stats_valid_data():
    """
    Test the `get_berry_stats` function when valid berry data is fetched from PokeAPI.

    This test mocks the cache and PokeAPI response to simulate valid berry data.
    It ensures that:
    - `fetch_all_berries` is called once.
    - Cache is updated with the correct statistics.
    - The statistics returned include correct values for berry names, growth times,
    variance, mean, and frequency growth times.
    """
    with patch('app.cache.cache_handler.RedisCacheHandler.get', return_value=None), \
        patch('app.cache.cache_handler.RedisCacheHandler.set', return_value=None) as mock_cache_set:
        
        mock_berries = [
            {'name': 'cheri', 'growth_time': 3},
            {'name': 'pecha', 'growth_time': 5},
            {'name': 'oran', 'growth_time': 7},
        ]
        
        with patch('app.services.berry_service.fetch_all_berries', new=AsyncMock(return_value=mock_berries)) as mock_fetch:
            stats = await get_berry_stats()
            
            mock_fetch.assert_called_once()
            mock_cache_set.assert_called_once_with("berry_stats", stats)
        
        assert stats["berries_names"] == ["cheri", "pecha", "oran"]
        assert stats["min_growth_time"] == 3
        assert stats["median_growth_time"] == 5
        assert stats["max_growth_time"] == 7
        assert stats["variance_growth_time"] == 4.0
        assert stats["mean_growth_time"] == 5.0
        assert stats["frequency_growth_time"] == {"3": 1, "5": 1, "7": 1}


@pytest.mark.asyncio
async def test_get_berry_stats_no_data():
    """
    Test the `get_berry_stats` function when no berry data is available from PokeAPI.

    This test mocks the cache and simulates an empty response from PokeAPI.
    It ensures that:
    - `fetch_all_berries` is called once.
    - The statistics returned have no berry names, and all growth time values are set to None.
    - Frequency growth time is an empty dictionary.
    """
    with patch('app.cache.cache_handler.RedisCacheHandler.get', return_value=None), \
        patch('app.cache.cache_handler.RedisCacheHandler.set', return_value=None):
        
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
    """
    Test the `get_berry_stats` function when berry data is fetched from cache.

    This test mocks the cache to simulate a scenario where berry statistics are retrieved from the cache.
    It ensures that:
    - The function returns the cached data directly without calling `fetch_all_berries`.
    - The returned statistics match the cached data.
    """
    cached_stats = {
        "berries_names": ["cached_cheri"],
        "min_growth_time": 1,
        "max_growth_time": 1,
        "mean_growth_time": 1.0,
        "variance_growth_time": 0.0,
        "frequency_growth_time": {"1": 1}
    }
    
    with patch('app.cache.cache_handler.RedisCacheHandler.get', return_value=cached_stats):
        stats = await get_berry_stats()
        
    assert stats == cached_stats