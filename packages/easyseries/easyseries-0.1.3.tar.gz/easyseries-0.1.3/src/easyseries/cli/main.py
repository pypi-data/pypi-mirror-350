"""CLI interface for EasySeries."""

import asyncio
import json
from pathlib import Path

import typer
from rich.console import Console
from rich.json import JSON
from rich.panel import Panel
from rich.table import Table

from easyseries import __version__
from easyseries.core.config import settings
from easyseries.http.client import http_client
from easyseries.http.utils import is_valid_url

app = typer.Typer(
    name="easyseries",
    help="EasySeries - HTTP utility toolkit with CLI support",
    add_completion=False,
)
console = Console()


@app.command()
def version() -> None:
    """Show version information."""
    console.print(f"EasySeries version: {__version__}")


@app.command()
def config() -> None:
    """Show current configuration."""
    config_dict = settings.to_dict()

    table = Table(title="EasySeries Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")

    for key, value in config_dict.items():
        table.add_row(key, str(value))

    console.print(table)


@app.command()
def request(
    url: str = typer.Argument(..., help="URL to request"),
    method: str = typer.Option("GET", "--method", "-m", help="HTTP method"),
    headers: str | None = typer.Option(
        None, "--headers", "-H", help="Headers as JSON string"
    ),
    data: str | None = typer.Option(
        None, "--data", "-d", help="Request data as JSON string"
    ),
    output: Path | None = typer.Option(None, "--output", "-o", help="Output file path"),
    pretty: bool = typer.Option(True, "--pretty/--no-pretty", help="Pretty print JSON"),
) -> None:
    asyncio.run(request_async(url, method, headers, data, output, pretty))


async def request_async(
    url: str,
    method: str = "GET",
    headers: str | None = None,
    data: str | None = None,
    output: Path | None = None,
    pretty: bool = True,
) -> None:
    """Make HTTP request."""
    if not is_valid_url(url):
        console.print(f"[red]Invalid URL: {url}[/red]")
        raise typer.Exit(1)

    # Parse headers
    request_headers = {}
    if headers:
        try:
            request_headers = json.loads(headers)
        except json.JSONDecodeError:
            console.print("[red]Invalid JSON in headers[/red]")
            raise typer.Exit(1)

    # Parse data
    request_data = None
    if data:
        try:
            request_data = json.loads(data)
        except json.JSONDecodeError:
            console.print("[red]Invalid JSON in data[/red]")
            raise typer.Exit(1)

    async with http_client() as client:
        try:
            response = await client._make_request(
                method.upper(), url, headers=request_headers, json=request_data
            )

            # Prepare response info
            response_info = {
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "url": str(response.url),
            }

            # Try to parse JSON
            try:
                response_info["json"] = await response.json()
            except Exception as e:
                console.print(f"[red]Invalid JSON: {e}[/red]")
                response_info["text"] = await response.text

            # Output handling
            if output:
                with open(output, "w") as f:
                    json.dump(response_info, f, indent=2)
                console.print(f"[green]Response saved to {output}[/green]")
            else:
                if pretty:
                    console.print(
                        Panel(JSON.from_data(response_info), title="Response")
                    )
                else:
                    console.print(json.dumps(response_info))

        except Exception as e:
            console.print(f"[red]Request failed: {e}[/red]")
            raise typer.Exit(1)


@app.command()
def benchmark(
    url: str = typer.Argument(..., help="URL to benchmark"),
    requests: int = typer.Option(10, "--requests", "-n", help="Number of requests"),
    concurrency: int = typer.Option(
        1, "--concurrency", "-c", help="Concurrent requests"
    ),
) -> None:
    """Benchmark HTTP endpoint."""
    if not is_valid_url(url):
        console.print(f"[red]Invalid URL: {url}[/red]")
        raise typer.Exit(1)

    async def run_benchmark() -> None:
        async with http_client() as client:
            semaphore = asyncio.Semaphore(concurrency)

            async def make_single_request() -> float:
                async with semaphore:
                    import time

                    start = time.time()
                    try:
                        await client.get(url)
                        return time.time() - start
                    except Exception:
                        return -1

            console.print(
                f"[yellow]Running benchmark: {requests} requests with concurrency {concurrency}[/yellow]"
            )

            # Run all requests
            tasks = [make_single_request() for _ in range(requests)]
            results = await asyncio.gather(*tasks)

            # Calculate statistics
            successful = [r for r in results if r >= 0]
            failed = len(results) - len(successful)

            if successful:
                avg_time = sum(successful) / len(successful)
                min_time = min(successful)
                max_time = max(successful)

                table = Table(title="Benchmark Results")
                table.add_column("Metric", style="cyan")
                table.add_column("Value", style="green")

                table.add_row("Total Requests", str(requests))
                table.add_row("Successful", str(len(successful)))
                table.add_row("Failed", str(failed))
                table.add_row("Average Time", f"{avg_time:.3f}s")
                table.add_row("Min Time", f"{min_time:.3f}s")
                table.add_row("Max Time", f"{max_time:.3f}s")

                console.print(table)
            else:
                console.print("[red]All requests failed[/red]")

    asyncio.run(run_benchmark())


if __name__ == "__main__":
    app()
