#!/usr/bin/env python3

# Third party imports
from decouple import config
from typer import echo

# Standard library imports
from os import path, mkdir


def create_dir_if_not_extant(path_to_dir: str) -> None:

    echo()
    echo(f"Checking for directory {path_to_dir}...")

    if not path.exists(path_to_dir):
        mkdir(path_to_dir)
        echo(f"\tCreated {path_to_dir}")
    else:
        echo(f"\t{path_to_dir} already exists.")

    echo()


def get_local_path(path):
    if path is None:
        local_repo = config("LINK_PARENT_DIR")
    else:
        local_repo = path
    return local_repo
