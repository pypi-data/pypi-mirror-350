"""Tests for CLI interface."""

from unittest.mock import AsyncMock, patch

import pytest
from typer.testing import CliRunner

from easyseries.cli.main import app, request_async

runner = CliRunner()


class TestCLI:
    """Test CLI functionality."""

    def test_version_command(self):
        """Test version command."""
        result = runner.invoke(app, ["version"])
        assert result.exit_code == 0
        assert "EasySeries version" in result.stdout

    def test_config_command(self):
        """Test config command."""
        result = runner.invoke(app, ["config"])
        assert result.exit_code == 0
        assert "Configuration" in result.stdout

    @pytest.mark.asyncio
    @patch("easyseries.cli.main.http_client")
    async def test_request_async(self, mock_client):
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.headers = {"content-type": "application/json"}
        mock_response.url = "https://httpbin.org/get"
        mock_response.json = AsyncMock(return_value={"args": {}})
        mock_response.text = AsyncMock(return_value="{}")

        mock_client_instance = AsyncMock()
        mock_client_instance._make_request.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        await request_async("https://httpbin.org/get")

    def test_request_invalid_url(self):
        """Test request with invalid URL."""
        result = runner.invoke(app, ["request", "invalid-url"])
        assert result.exit_code == 1
        assert "Invalid URL" in result.stdout

    @patch("easyseries.cli.main.http_client")
    def test_benchmark_command(self, mock_client):
        """Test benchmark command."""
        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = AsyncMock()
        mock_client.return_value.__aenter__.return_value = mock_client_instance

        result = runner.invoke(
            app,
            [
                "benchmark",
                "https://httpbin.org/get",
                "--requests",
                "2",
                "--concurrency",
                "1",
            ],
        )
        assert result.exit_code == 0
