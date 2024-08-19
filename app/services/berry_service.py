import logging
import statistics
from app.data_providers.pokeapi_provider import fetch_all_berries
from app.cache.cache_handler import RedisCacheHandler

cache = RedisCacheHandler()
logging.basicConfig(level=logging.INFO)

async def get_berry_stats():
    cached_data = cache.get("berry_stats")
    if cached_data:
        logging.info("Fetching data from cache.")
        return cached_data
    
    logging.info("Fetching data from PokeAPI.")
    berries = await fetch_all_berries()
    growth_times = [berry['growth_time'] for berry in berries if 'growth_time' in berry]
    
    stats = {
        "berries_names": [berry['name'] for berry in berries],
        "min_growth_time": int(min(growth_times)) if growth_times else None,
        "median_growth_time": float(statistics.median(growth_times)) if growth_times else None,
        "max_growth_time": int(max(growth_times)) if growth_times else None,
        "variance_growth_time": float(statistics.variance(growth_times)) if len(growth_times) > 1 else None,
        "mean_growth_time": float(statistics.mean(growth_times)) if growth_times else None,
        "frequency_growth_time": {str(x): int(growth_times.count(x)) for x in set(growth_times)}
    }

    cache.set("berry_stats", stats)
    logging.info("Storing data in cache.")
    return stats