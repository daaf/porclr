#!/usr/bin/env python3
"""
Link or copy Docker Compose files from Portainer to a directory of your choosing.

Usage:
    porclr link [<path>] [--username <username>] [--password <password>]
    porclr copy [<path>] [--username <username>] [--password <password>]

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
    """Prints the name of the app and the app version.

    :param value: Identifies if the callback function should be executed.
    :raises typer.Exit: If the app name and version are printed, exits.
    """
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
    """Calls `_version_callback` to print the app name and version."""
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
    """Creates a `Link` object from the command line arguments, then calls the
    `Link` object's `execute` method to create the links.

    :param path: Optional. The path on the local filesystem where the links
        and their associated subdirectories should be created.
    :param username: Optional. The username to use to authenticate with Portainer.
        If not provided as a command line argument, the CLI will prompt for
        the username.
    :param password: Optional. The password to use to authenticate with Portainer.
        If not provided as a command line argument, the CLI will prompt for
        the password.
    """
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
    """Creates a `Copy` object from the command line arguments, then calls the
    `Copy` object's `execute` method to create the links.

    :param path: Optional. The path on the local filesystem where the copies
        and their associated subdirectories should be created.
    :param username: Optional. The username to use to authenticate with Portainer.
        If not provided as a command line argument, the CLI will prompt for
        the username.
    :param password: Optional. The password to use to authenticate with Portainer.
        If not provided as a command line argument, the CLI will prompt for
        the password.
    """
    try:
        copy_action = actions.Copy(path=path, username=username, password=password)
        copy_action.execute()
    except:
        return
