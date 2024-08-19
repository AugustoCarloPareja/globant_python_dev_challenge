# -*- coding: utf-8 -*-
import pytest
from unittest.mock import patch, AsyncMock
from app.services.berry_service import get_berry_stats
from app.models.berry_models import BerryStatsResponseModel

@pytest.mark.asyncio
async def test_get_berry_stats_valid_data():
    """
    Test the `get_berry_stats` function when valid berry data is fetched from PokeAPI.
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
            mock_cache_set.assert_called_once_with("berry_stats", stats.model_dump())  # Convert Pydantic model to dict
        
        assert stats.berries_names == ["cheri", "pecha", "oran"]
        assert stats.min_growth_time == 3
        assert stats.median_growth_time == 5
        assert stats.max_growth_time == 7
        assert stats.variance_growth_time == 4.0
        assert stats.mean_growth_time == 5.0
        assert stats.frequency_growth_time == {3: 1, 5: 1, 7: 1}

@pytest.mark.asyncio
async def test_get_berry_stats_no_data():
    """
    Test the `get_berry_stats` function when no berry data is available from PokeAPI.
    """
    with patch('app.cache.cache_handler.RedisCacheHandler.get', return_value=None), \
        patch('app.cache.cache_handler.RedisCacheHandler.set', return_value=None):

        mock_berries = []
        with patch('app.services.berry_service.fetch_all_berries', new=AsyncMock(return_value=mock_berries)) as mock_fetch:
            stats = await get_berry_stats()
            
            mock_fetch.assert_called_once()
            
        assert stats.berries_names == []
        assert stats.min_growth_time is None
        assert stats.max_growth_time is None
        assert stats.mean_growth_time is None
        assert stats.variance_growth_time is None
        assert stats.frequency_growth_time == {}

@pytest.mark.asyncio
async def test_get_berry_stats_with_cache():
    """
    Test the `get_berry_stats` function when berry data is fetched from cache.
    """
    cached_stats = BerryStatsResponseModel(
        berries_names=["cached_cheri"],
        min_growth_time=1,
        max_growth_time=1,
        mean_growth_time=1.0,
        variance_growth_time=0.0,
        frequency_growth_time={1: 1}
    )
    
    with patch('app.cache.cache_handler.RedisCacheHandler.get', return_value=cached_stats.dict()):
        stats = await get_berry_stats()
    
    assert stats == cached_stats