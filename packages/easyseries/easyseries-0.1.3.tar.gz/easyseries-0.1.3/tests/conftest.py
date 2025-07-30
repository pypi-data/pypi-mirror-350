"""Pytest configuration and fixtures."""

from unittest.mock import AsyncMock

import httpx
import pytest
import respx

from easyseries.http.client import HTTPClient


@pytest.fixture
def mock_response():
    """Mock HTTP response."""
    response = AsyncMock(spec=httpx.Response)
    response.status_code = 200
    response.json.return_value = {"message": "success"}
    response.text = '{"message": "success"}'
    response.url = "https://api.example.com/test"
    response.headers = {"content-type": "application/json"}
    return response


@pytest.fixture
async def http_client():
    """HTTP client fixture."""
    client = HTTPClient(base_url="https://api.example.com")
    yield client
    await client.close()


@pytest.fixture
def respx_mock():
    """respx mock fixture."""
    with respx.mock:
        yield respx
