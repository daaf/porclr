#!/usr/bin/env python3
"""
Create links to Portainer's Docker Compose files in a specified directory.

Usage:
    porclr link

Options:
    -h --help   Show this help documentation.
    -l --link   Link Compose files
"""

# Third party imports
import typer
from typing import Optional
from decouple import config

# Local imports
from link_portainer_compose_files import link_files
from __init__ import __app_name__, __app_version__

app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__app_version__}")
        raise typer.Exit()


@app.command()
def link(path: Optional[str] = typer.Argument(None)) -> None:
    portainer_compose_dir = config("PORTAINER_COMPOSE_DIR")

    if path is None:
        local_repo = config("LINK_PARENT_DIR")
    else:
        local_repo = path

    link_files(portainer_compose_dir, local_repo)


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return
