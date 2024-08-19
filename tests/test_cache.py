import time
from app.cache.cache_handler import cache
from cachetools import TTLCache

def test_cache_set_and_get():
    cache['test_key'] = 'test_value'
    assert cache['test_key'] == 'test_value'

def test_cache_expiry():
    test_cache = TTLCache(maxsize=100, ttl=1)
    
    test_cache['expiring_key'] = 'will_expire'
    time.sleep(2)
    
    assert 'expiring_key' not in test_cache