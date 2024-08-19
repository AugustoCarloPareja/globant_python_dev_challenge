import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

POKEAPI_BERRY_URL = os.getenv("POKEAPI_BERRY_URL")

async def fetch_all_berries():
    try:
        response = requests.get(POKEAPI_BERRY_URL)
        response.raise_for_status()
        
        berries_data = response.json()['results']
        
        berries = []
        for berry_data in berries_data:
            berry_details = requests.get(berry_data['url']).json()
            berries.append({
                'name': berry_details['name'],
                'growth_time': berry_details['growth_time']
            })
        
        return berries

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data from PokeAPI: {e}")
        return []

    except ValueError as e:
        logger.error(f"Value error: {e}")
        return []

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return []