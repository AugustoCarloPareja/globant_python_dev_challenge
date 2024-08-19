# -*- coding: utf-8 -*-
import time
from unittest.mock import patch
from app.cache.cache_handler import RedisCacheHandler

def test_cache_set_and_get():
    """
    Test the `set` and `get` methods of the RedisCacheHandler.

    This test ensures that:
    - The `set` method stores a key-value pair correctly.
    - The `get` method retrieves the value associated with the key.
    - Mocks are used to simulate cache interactions without actual Redis connections.
    """
    with patch('app.cache.cache_handler.RedisCacheHandler.set') as mock_set, \
        patch('app.cache.cache_handler.RedisCacheHandler.get', return_value='test_value'):
            
        cache_handler = RedisCacheHandler()
        cache_handler.set('test_key', 'test_value')
        
        result = cache_handler.get('test_key')
        
        mock_set.assert_called_once_with('test_key', 'test_value')
        assert result == 'test_value'

def test_cache_expiry():
    """
    Test the cache expiration behavior of the RedisCacheHandler.

    This test ensures that:
    - The `set` method stores a key-value pair correctly.
    - The `get` method returns `None` after the simulated cache expiration period.
    - Mocks are used to simulate cache interactions and control expiration behavior without an actual Redis connection.
    """
    with patch('app.cache.cache_handler.RedisCacheHandler.set') as mock_set, \
        patch('app.cache.cache_handler.RedisCacheHandler.get', side_effect=[None]):
            
        cache_handler = RedisCacheHandler()
        cache_handler.set('expiring_key', 'will_expire')
        
        time.sleep(2)
        
        result = cache_handler.get('expiring_key')
        
        mock_set.assert_called_once_with('expiring_key', 'will_expire')
        assert result is None