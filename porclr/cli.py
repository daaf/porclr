#!/usr/bin/env python3
"""
Create links to Portainer's Docker Compose files in a specified directory.

Usage:
    porclr link

Options:
    -h --help   Show this help documentation.
    -v --version See porclr's version
"""

# Third party imports
import typer
from typing import Optional
from decouple import config

# Local imports
from porclr import __app_name__, __app_version__, link_portainer_compose_files

app = typer.Typer()

link_files = link_portainer_compose_files.link_files


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


@app.command()
def copy(
    endpoint: str = typer.Argument(...),
    username: str = typer.Option(
        ...,
        "--username",
        "-u",
        help="The username to use to authenticate with Portainer.",
        prompt=True,
    ),
) -> None:
    pass


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
