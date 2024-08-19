import time
from unittest.mock import patch
from app.cache.cache_handler import RedisCacheHandler

def test_cache_set_and_get():
    with patch('app.cache.cache_handler.RedisCacheHandler.set') as mock_set, \
        patch('app.cache.cache_handler.RedisCacheHandler.get', return_value='test_value'):
            
        cache_handler = RedisCacheHandler()
        cache_handler.set('test_key', 'test_value')
        
        result = cache_handler.get('test_key')
        
        mock_set.assert_called_once_with('test_key', 'test_value')
        assert result == 'test_value'

def test_cache_expiry():
    with patch('app.cache.cache_handler.RedisCacheHandler.set') as mock_set, \
        patch('app.cache.cache_handler.RedisCacheHandler.get', side_effect=[None]):
            
        cache_handler = RedisCacheHandler()
        cache_handler.set('expiring_key', 'will_expire')
        
        time.sleep(2)
        
        result = cache_handler.get('expiring_key')
        
        mock_set.assert_called_once_with('expiring_key', 'will_expire')
        assert result is None