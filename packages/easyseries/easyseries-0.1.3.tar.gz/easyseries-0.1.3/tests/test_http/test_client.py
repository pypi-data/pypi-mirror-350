"""Tests for HTTP client."""

import time
from unittest.mock import patch

import httpx
import pytest

from easyseries.core.exceptions import HTTPClientError, RateLimitError
from easyseries.http.client import HTTPClient, http_client


class TestHTTPClient:
    """Test HTTP client functionality."""

    @pytest.mark.asyncio
    async def test_client_initialization(self):
        """Test client initialization."""
        client = HTTPClient(
            base_url="https://api.example.com", timeout=30.0, max_retries=3
        )

        assert client.base_url == "https://api.example.com"
        assert client.timeout == 30.0
        assert client.max_retries == 3

        await client.close()

    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test async context manager."""
        async with http_client(base_url="https://api.example.com") as client:
            assert isinstance(client, HTTPClient)
            assert client.base_url == "https://api.example.com"

    @pytest.mark.asyncio
    async def test_get_request(self, respx_mock):
        """Test GET request."""
        respx_mock.get("https://api.example.com/users").mock(
            return_value=httpx.Response(200, json={"users": []})
        )

        async with http_client(base_url="https://api.example.com") as client:
            response = await client.get("/users")
            assert response.status_code == 200
            assert response.json() == {"users": []}

    @pytest.mark.asyncio
    async def test_post_request(self, respx_mock):
        """Test POST request."""
        respx_mock.post("https://api.example.com/users").mock(
            return_value=httpx.Response(201, json={"id": 1, "name": "John"})
        )

        async with http_client(base_url="https://api.example.com") as client:
            response = await client.post("/users", json={"name": "John"})
            assert response.status_code == 201
            assert response.json()["name"] == "John"

    @pytest.mark.asyncio
    async def test_retry_logic(self, respx_mock):
        """Test retry logic on server errors."""
        # First request fails, second succeeds
        respx_mock.get("https://api.example.com/flaky").mock(
            side_effect=[
                httpx.Response(500, text="Server Error"),
                httpx.Response(200, json={"status": "ok"}),
            ]
        )

        async with http_client(
            base_url="https://api.example.com", max_retries=2
        ) as client:
            response = await client.get("/flaky")
            assert response.status_code == 200
            assert response.json()["status"] == "ok"

    @pytest.mark.asyncio
    async def test_http_error_handling(self, respx_mock):
        """Test HTTP error handling."""
        respx_mock.get("https://api.example.com/error").mock(
            return_value=httpx.Response(404, text="Not Found")
        )

        async with http_client(base_url="https://api.example.com") as client:
            with pytest.raises(HTTPClientError) as exc_info:
                await client.get("/error")

            assert "HTTP 404" in str(exc_info.value)
            assert exc_info.value.details["status_code"] == 404

    @pytest.mark.asyncio
    async def test_rate_limiting(self):
        """Test rate limiting functionality."""
        with patch("easyseries.core.config.settings.enable_metrics", True):
            client = HTTPClient(rate_limit=2)

            now = time.time()
            # Simulate two requests just within the 60-second window
            client._request_times = [now - 10, now - 5]

            with pytest.raises(RateLimitError):
                client._check_rate_limit()

            await client.close()

    @pytest.mark.asyncio
    async def test_metrics_collection(self, respx_mock):
        """Test metrics collection."""
        respx_mock.get("https://api.example.com/test").mock(
            return_value=httpx.Response(200, json={"test": True})
        )

        with patch("easyseries.core.config.settings.enable_metrics", True):
            async with http_client(base_url="https://api.example.com") as client:
                await client.get("/test")

                metrics = client.get_metrics()
                assert len(metrics) == 1
                assert metrics[0].method == "GET"
                assert metrics[0].status_code == 200
                assert metrics[0].url == "https://api.example.com/test"
