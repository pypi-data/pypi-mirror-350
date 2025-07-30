"""HTTP utility functions."""

import json
from typing import Any
from urllib.parse import urljoin, urlparse

import httpx
from pydantic import BaseModel, ValidationError

from easyseries.core.exceptions import ValidationError as EasySeriesValidationError


def is_valid_url(url: str) -> bool:
    """Check if URL is valid."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def join_url(base: str, path: str) -> str:
    """Join base URL with path."""
    return urljoin(base, path)


def extract_json(response: httpx.Response) -> Any:
    """Extract JSON from response with error handling."""
    try:
        return response.json()
    except json.JSONDecodeError as e:
        raise EasySeriesValidationError(
            "Failed to decode JSON response",
            details={"response_text": response.text[:500]},
            original_error=e,
        )


def validate_response_model(
    response: httpx.Response, model: type[BaseModel]
) -> BaseModel:
    """Validate response against Pydantic model."""
    try:
        data = extract_json(response)
        return model.model_validate(data)
    except ValidationError as e:
        raise EasySeriesValidationError(
            f"Response validation failed for {model.__name__}",
            details={"validation_errors": e.errors()},
            original_error=e,
        )


def format_headers(headers: dict[str, str] | None) -> str:
    """Format headers for logging."""
    if not headers:
        return "No headers"

    formatted = []
    for key, value in headers.items():
        # Mask sensitive headers
        if key.lower() in ("authorization", "x-api-key", "cookie"):
            value = "*" * len(value)
        formatted.append(f"{key}: {value}")

    return "\n".join(formatted)


def build_query_params(params: dict[str, Any]) -> dict[str, str]:
    """Build query parameters, handling various types."""
    result = {}
    for key, value in params.items():
        if value is None:
            continue
        elif isinstance(value, list | tuple):
            # Convert lists to comma-separated strings
            result[key] = ",".join(str(v) for v in value)
        elif isinstance(value, bool):
            result[key] = str(value).lower()
        else:
            result[key] = str(value)

    return result
