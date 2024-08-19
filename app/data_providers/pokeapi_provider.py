# -*- coding: utf-8 -*-
import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

POKEAPI_BERRY_URL = os.getenv("POKEAPI_BERRY_URL")

async def fetch_all_berries():
    """
    Fetch all berries data from the PokeAPI.

    This function fetches a list of all berries available from the PokeAPI by 
    sending a request to the provided POKEAPI_BERRY_URL. For each berry, it fetches 
    additional details, such as the berry's name and growth time, and stores them in a list.

    Returns:
        list: A list of dictionaries containing each berry's name and growth time.
        In case of errors, it returns an empty list.

    Error Handling:
        - If a `RequestException` occurs (e.g., network error, invalid URL), logs the error and returns an empty list.
        - If a `ValueError` occurs (e.g., parsing issues), logs the error and returns an empty list.
        - If any other unexpected error occurs, logs the error and returns an empty list.
    """
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