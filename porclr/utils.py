#!/usr/bin/env python3

# Third party imports
from typer import echo

# Standard library imports
from os import path, mkdir


def create_dir_if_not_extant(path_to_dir: str) -> None:
    echo(f"\nChecking for directory {path_to_dir}...")

    if not path.exists(path_to_dir):
        try:
            mkdir(path_to_dir)
            echo(f"\tCreated {path_to_dir}\n")
        except:
            echo("Invalid path.")
    else:
        echo(f"\t{path_to_dir} already exists.")
