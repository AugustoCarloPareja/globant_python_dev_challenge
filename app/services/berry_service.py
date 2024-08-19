# -*- coding: utf-8 -*-
import logging
import statistics
from app.data_providers.pokeapi_provider import fetch_all_berries
from app.cache.cache_handler import RedisCacheHandler
from app.models.berry_models import BerryStatsResponseModel

cache = RedisCacheHandler()
logging.basicConfig(level=logging.INFO)

async def get_berry_stats():
    """
    Fetch berry growth statistics, either from the cache or by retrieving data from PokeAPI.

    This function first checks if the berry statistics are available in the Redis cache.
    If cached data exists, it is returned. Otherwise, it fetches the data from PokeAPI, computes
    various statistics on berry growth times (like min, median, max, variance, mean, and frequency), 
    stores the results in Redis for caching, and then returns the computed statistics using the 
    BerryStatsResponseModel.

    Returns:
        BerryStatsResponseModel: A Pydantic model containing berry names and their growth statistics.
    """
    cached_data = cache.get("berry_stats")
    if cached_data:
        logging.info("Fetching data from cache.")
        return BerryStatsResponseModel(**cached_data)
    
    logging.info("Fetching data from PokeAPI.")
    berries = await fetch_all_berries()
    growth_times = [berry['growth_time'] for berry in berries if 'growth_time' in berry]
    
    stats = BerryStatsResponseModel(
        berries_names=[berry['name'] for berry in berries],
        min_growth_time=int(min(growth_times)) if growth_times else None,
        median_growth_time=float(statistics.median(growth_times)) if growth_times else None,
        max_growth_time=int(max(growth_times)) if growth_times else None,
        variance_growth_time=float(statistics.variance(growth_times)) if len(growth_times) > 1 else None,
        mean_growth_time=float(statistics.mean(growth_times)) if growth_times else None,
        frequency_growth_time={str(x): int(growth_times.count(x)) for x in set(growth_times)}
    )
    
    cache.set("berry_stats", stats.model_dump())
    logging.info("Storing data in cache.")
    
    return stats