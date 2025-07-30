"""Configuration management for EasySeries."""

from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="EASYSERIES_",
        case_sensitive=False,
        extra="ignore",
    )

    # HTTP Client Settings
    timeout: float = Field(
        default=30.0, description="Default request timeout in seconds"
    )
    max_retries: int = Field(default=3, description="Maximum number of retries")
    base_url: str | None = Field(default=None, description="Base URL for requests")

    # Headers
    user_agent: str = Field(
        default="EasySeries/0.1.0", description="Default User-Agent header"
    )

    # Rate limiting
    rate_limit_requests: int = Field(
        default=100, description="Requests per minute limit"
    )

    # Logging
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format string",
    )

    # Feature flags
    enable_caching: bool = Field(default=False, description="Enable response caching")
    enable_metrics: bool = Field(default=False, description="Enable metrics collection")

    def to_dict(self) -> Any:
        """Convert settings to dictionary."""
        return self.model_dump()


# Global settings instance
settings = Settings()
