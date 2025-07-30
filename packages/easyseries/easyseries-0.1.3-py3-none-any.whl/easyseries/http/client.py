"""HTTP client implementation using httpx."""

import asyncio
import time
from contextlib import asynccontextmanager
from typing import Any

import httpx
from pydantic import BaseModel, Field

from easyseries.core.config import settings
from easyseries.core.exceptions import HTTPClientError, RateLimitError


class RequestMetrics(BaseModel):
    """Request metrics model."""

    url: str
    method: str
    status_code: int
    duration: float = Field(description="Request duration in seconds")
    timestamp: float = Field(default_factory=time.time)
    retries: int = 0


class HTTPClient:
    """Async HTTP client with advanced features."""

    def __init__(
        self,
        base_url: str | None = None,
        timeout: float = 30.0,
        max_retries: int = 3,
        rate_limit: int = 100,
        headers: dict[str, str] | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize HTTP client.
        Args:
            base_url: Base URL for all requests
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries
            rate_limit: Requests per minute limit
            headers: Default headers
            **kwargs: Additional httpx.AsyncClient arguments
        """
        self.base_url = base_url or settings.base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.rate_limit = rate_limit

        # Default headers
        default_headers = {
            "User-Agent": settings.user_agent,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if headers:
            default_headers.update(headers)

        # Rate limiting
        self._request_times: list[float] = []

        # Metrics
        self._metrics: list[RequestMetrics] = []

        # HTTP client configuration
        client_kwargs = {
            "base_url": self.base_url,
            "timeout": httpx.Timeout(timeout),
            "headers": default_headers,
            "follow_redirects": True,
            **kwargs,
        }

        self._client: httpx.AsyncClient | None = None
        self._client_kwargs = client_kwargs

    async def __aenter__(self) -> "HTTPClient":
        """Async context manager entry."""
        await self._ensure_client()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.close()

    async def _ensure_client(self) -> None:
        """Ensure HTTP client is initialized."""
        if self._client is None:
            self._client = httpx.AsyncClient(**self._client_kwargs)

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None

    def _check_rate_limit(self) -> None:
        """Check if rate limit is exceeded."""
        now = time.time()
        # Remove requests older than 1 minute
        self._request_times = [t for t in self._request_times if now - t < 60]

        if len(self._request_times) >= self.rate_limit:
            raise RateLimitError(
                f"Rate limit of {self.rate_limit} requests per minute exceeded"
            )

        self._request_times.append(now)

    async def _make_request(
        self, method: str, url: str, retries: int = 0, **kwargs: Any
    ) -> httpx.Response:
        """Make HTTP request with retry logic."""
        await self._ensure_client()

        if settings.enable_metrics:
            self._check_rate_limit()

        start_time = time.time()

        try:
            if self._client is None:
                raise RuntimeError("Client not initialized")
            response = await self._client.request(method, url, **kwargs)
            response.raise_for_status()

            # Record metrics
            if settings.enable_metrics:
                duration = time.time() - start_time
                metrics = RequestMetrics(
                    url=str(response.url),
                    method=method.upper(),
                    status_code=response.status_code,
                    duration=duration,
                    retries=retries,
                )
                self._metrics.append(metrics)

            return response

        except httpx.HTTPStatusError as e:
            if retries < self.max_retries and e.response.status_code >= 500:
                await asyncio.sleep(2**retries)  # Exponential backoff
                return await self._make_request(method, url, retries + 1, **kwargs)
            raise HTTPClientError(
                f"HTTP {e.response.status_code}: {e.response.text}",
                details={
                    "status_code": e.response.status_code,
                    "url": str(e.response.url),
                    "method": method.upper(),
                },
                original_error=e,
            )
        except Exception as e:
            raise HTTPClientError(
                f"Request failed: {e!s}",
                details={"url": url, "method": method.upper()},
                original_error=e,
            )

    async def get(
        self, url: str, params: dict[str, Any] | None = None, **kwargs: Any
    ) -> httpx.Response:
        """Make GET request."""
        return await self._make_request("GET", url, params=params, **kwargs)

    async def post(
        self,
        url: str,
        json: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> httpx.Response:
        """Make POST request."""
        return await self._make_request("POST", url, json=json, data=data, **kwargs)

    async def put(
        self,
        url: str,
        json: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> httpx.Response:
        """Make PUT request."""
        return await self._make_request("PUT", url, json=json, data=data, **kwargs)

    async def patch(
        self,
        url: str,
        json: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> httpx.Response:
        """Make PATCH request."""
        return await self._make_request("PATCH", url, json=json, data=data, **kwargs)

    async def delete(self, url: str, **kwargs: Any) -> httpx.Response:
        """Make DELETE request."""
        return await self._make_request("DELETE", url, **kwargs)

    def get_metrics(self) -> list[RequestMetrics]:
        """Get request metrics."""
        return self._metrics.copy()

    def clear_metrics(self) -> None:
        """Clear request metrics."""
        self._metrics.clear()


@asynccontextmanager
async def http_client(**kwargs: Any) -> Any:
    """Async context manager for HTTP client."""
    client = HTTPClient(**kwargs)
    try:
        yield client
    finally:
        await client.close()
