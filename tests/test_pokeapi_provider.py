import pytest
import requests
from unittest.mock import patch
from app.data_providers.pokeapi_provider import fetch_all_berries

@pytest.mark.asyncio
async def test_fetch_all_berries_valid():
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
    with patch('requests.get', side_effect=requests.exceptions.RequestException):
        berries = await fetch_all_berries()
    
    assert berries == []