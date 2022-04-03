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
from porclr import actions, __app_name__, __version__
from porclr import portainer_queries
from porclr import utils
from porclr.actions import copy_compose_files

app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.command()
def link(path: Optional[str] = typer.Argument(None)) -> None:
    portainer_compose_dir = config("PORTAINER_COMPOSE_DIR")
    local_path = utils.get_local_path(path)

    actions.link_compose_files(portainer_compose_dir, local_path)


@app.command()
def copy(
    url: str = typer.Argument(
        ..., help="The URL of the Portainer instance, including port number."
    ),
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
    ),
) -> None:
    auth_token = portainer_queries.get_auth_token(url, username, password)
    stack_list = portainer_queries.get_stack_list(url, auth_token=auth_token)
    local_path = utils.get_local_path(path)

    actions.copy_compose_files(url, local_path, stack_list, auth_token=auth_token)

    print(f"url: {url}")
    print(f"path: {path}")
    print(f"local_path: {local_path}")
    print(f"username: {username}")
    print(f"password: {password}")
    print(f"auth_token: {auth_token}")
    print(stack_list)


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
