import os
from cachetools import TTLCache

CACHE_TTL = int(os.getenv("CACHE_TTL"))
CACHE_MAXSIZE = int(os.getenv("CACHE_MAXSIZE"))

cache = TTLCache(maxsize=CACHE_MAXSIZE, ttl=CACHE_TTL)