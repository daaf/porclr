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

# Local imports
from porclr import actions, __app_name__, __version__

app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


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


@app.command()
def link(
    path: Optional[str] = typer.Argument(
        None,
        help="The path to the directory where the Compose file links should be created.",
    ),
    username: Optional[str] = typer.Option(
        ...,
        "--username",
        "-u",
        help="The username to use to authenticate with Portainer.",
        prompt=True,
    ),
    password: Optional[str] = typer.Option(
        ...,
        "--password",
        "-p",
        help="The password to use to authenticate with Portainer.",
        prompt=True,
        hide_input=True,
    ),
) -> None:
    try:
        link_action = actions.Link(path=path, username=username, password=password)
        link_action.execute()
    except:
        return


@app.command()
def copy(
    path: Optional[str] = typer.Argument(
        None,
        help="The path to the directory to which the Compose files should be copied.",
    ),
    username: Optional[str] = typer.Option(
        ...,
        "--username",
        "-u",
        help="The username to use to authenticate with Portainer.",
        prompt=True,
    ),
    password: Optional[str] = typer.Option(
        ...,
        "--password",
        "-p",
        help="The password to use to authenticate with Portainer.",
        prompt=True,
        hide_input=True,
    ),
) -> None:
    try:
        copy_action = actions.Copy(path=path, username=username, password=password)
        copy_action.execute()
    except:
        return
