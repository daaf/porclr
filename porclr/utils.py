#!/usr/bin/env python3

# Third party imports
from decouple import config

# Standard library imports
from os import path, mkdir


def get_compose_attribute_value(compose_file, keyword):
    """
    Get the value of an attribute from a Docker Compose file.

    :param compose_file: The Docker Compose file to search.
    :param keyword: The keyword of the value to retrieve.
    :returns: If the keyword is found, the value corresponding to the keyword.
    """
    with open(compose_file) as file:
        for line in file:
            if keyword in line:
                value = line.replace(f"{keyword}:", "").strip()
                return value


def create_dir_if_not_extant(path_to_dir: str) -> None:

    print()
    print(f"Checking for directory {path_to_dir}...")

    if not path.exists(path_to_dir):
        mkdir(path_to_dir)
        print(f"\tCreated {path_to_dir}")
    else:
        print(f"\t{path_to_dir} already exists.")

    print()


def create_compose_file_if_not_extant(path_to_dir: str) -> None:
    create_dir_if_not_extant(path_to_dir)


def get_local_path(path):
    if path is None:
        local_repo = config("LINK_PARENT_DIR")
    else:
        local_repo = path
    return local_repo
