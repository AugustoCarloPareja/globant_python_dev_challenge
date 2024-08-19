# -*- coding: utf-8 -*-
import pytest
import requests
from unittest.mock import patch
from app.data_providers.pokeapi_provider import fetch_all_berries

@pytest.mark.asyncio
async def test_fetch_all_berries_valid():
    """
    Test the `fetch_all_berries` function with valid data.

    This test simulates the behavior of fetching berries from the PokeAPI by:
    - Mocking the `requests.get` method to return a valid response with berry details.
    - Ensuring that the returned berry list contains the correct name and growth time.
    - Verifying that the correct number of berries is returned.
    """
    mock_response = {'results': [{'name': 'cheri', 'url': 'https://pokeapi.co/api/v2/berry/1/'}]}
    mock_berry_detail = {'name': 'cheri', 'growth_time': 3}
    
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.side_effect = [mock_response, mock_berry_detail]
        
        berries = await fetch_all_berries()
        
        assert len(berries) == 1
        assert berries[0]["name"] == "cheri"
        assert berries[0]["growth_time"] == 3

@pytest.mark.asyncio
async def test_fetch_all_berries_failure():
    """
    Test the `fetch_all_berries` function when the PokeAPI request fails.

    This test simulates a failed request to the PokeAPI by:
    - Mocking the `requests.get` method to raise a `RequestException`.
    - Verifying that an empty list of berries is returned when an error occurs.
    """
    with patch('requests.get', side_effect=requests.exceptions.RequestException):
        berries = await fetch_all_berries()
    
    assert berries == []