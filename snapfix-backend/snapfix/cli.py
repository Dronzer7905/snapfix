"""
snapfix/cli.py

Author: Snapfix Contributors
License: MIT

Typer CLI for Snapfix Engine.
"""

from __future__ import annotations

import asyncio
import json

import typer
import uvicorn
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from snapfix import __version__
from snapfix.config import load_config
from snapfix.constants import APP_NAME, DEFAULT_HOST, DEFAULT_PORT
from snapfix.db.cache import CacheLayer

console = Console()

app = typer.Typer(
    name=APP_NAME,
    help="Snapfix: Real-time AI-powered Python error analyzer.",
    no_args_is_help=True,
    add_completion=False,
)

cache_app = typer.Typer(help="Manage the analysis cache.")
app.add_typer(cache_app, name="cache")


@app.command()
def server(
    host: str = typer.Option(DEFAULT_HOST, "--host", help="Bind host"),
    port: int = typer.Option(DEFAULT_PORT, "--port", help="Bind port"),
    reload: bool = typer.Option(False, "--reload", help="Enable auto-reload (dev)"),
) -> None:
    """Start the Snapfix FastAPI server."""
    config = load_config()
    effective_host = host or config.server.host
    effective_port = port or config.server.port

    rprint(
        Panel(
            f"[bold green]Snapfix Engine v{__version__}[/] server starting\n"
            f"  [dim]http://{effective_host}:{effective_port}[/]",
            title="[bold]Snapfix[/]",
            border_style="green",
        )
    )

    uvicorn.run(
        "snapfix.server:app",
        host=effective_host,
        port=effective_port,
        reload=reload,
        log_level="info",
    )


@cache_app.command("stats")
def cache_stats() -> None:
    """Display cache statistics."""

    async def _stats() -> dict[str, int]:
        layer = CacheLayer()
        await layer.initialize()
        return await layer.stats()

    stats = asyncio.run(_stats())

    table = Table(title="Snapfix Cache Stats", show_header=True, header_style="bold cyan")
    table.add_column("Metric", style="dim")
    table.add_column("Value", justify="right")

    table.add_row("Cached analyses", str(stats["total_entries"]))
    table.add_row("Total cache hits", str(stats["total_hits"]))
    table.add_row("Total requests logged", str(stats["total_requests"]))

    console.print()
    console.print(table)
    console.print()


@app.command()
def version() -> None:
    """Print the Snapfix version."""
    rprint(f"Snapfix Engine [bold green]v{__version__}[/]")
