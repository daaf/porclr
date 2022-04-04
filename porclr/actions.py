#!/usr/bin/env python3

# Third party import
from argparse import ArgumentError
from decouple import config

# Standard library imports
import os

# Local imports
from porclr import portainer_queries, utils


def link_compose_file(path_to_original_compose_file, path_to_new_compose_file):

    if not os.path.exists(path_to_new_compose_file):
        os.link(path_to_original_compose_file, path_to_new_compose_file)

        print(
            f"\tCreated link to {path_to_original_compose_file} in {path_to_new_compose_file}."
        )
        print()

        return True

    print(f"\t{path_to_new_compose_file} already exists.")
    print()

    return False


def copy_compose_file(path_to_new_compose_file, url, stack_id, auth_token):

    if not os.path.exists(path_to_new_compose_file):
        compose_file = portainer_queries.get_compose_file(
            url, stack_id, auth_token=auth_token
        )
        with open(path_to_new_compose_file, "w") as file:
            file.write(compose_file)

        print(f"\tCopied docker-compose.yml to {path_to_new_compose_file}.")
        print()

        return True

    print(f"\t{path_to_new_compose_file} already exists.")
    print()

    return False


def execute_stack_action(
    action: str,
    url: str,
    path: str,
    username: str,
    password: str,
):
    auth_token = portainer_queries.get_auth_token(url, username, password)
    stack_list = portainer_queries.get_stack_list(url, auth_token=auth_token)
    local_path = utils.get_local_path(path)
    new_count = 0
    action_description = ""

    for stack in stack_list:
        stack_id = stack["id"]
        stack_name = stack["name"]
        path_to_stack_dir = f"{local_path}/{stack_name}"
        path_to_new_compose_file = f"{path_to_stack_dir}/docker-compose.yml"
        portainer_compose_dir = config("PORTAINER_COMPOSE_DIR")

        utils.create_dir_if_not_extant(path_to_stack_dir)

        print(f"Checking for docker-compose.yml at {path_to_new_compose_file}...")

        if action == "link":
            action_description = "links to "
            path_to_original_compose_file = (
                f"{portainer_compose_dir}/{stack_id}/docker-compose.yml"
            )
            result = link_compose_file(
                path_to_original_compose_file, path_to_new_compose_file
            )
        elif action == "copy":
            result = copy_compose_file(
                path_to_new_compose_file, url, stack_id, auth_token
            )
        else:
            raise ArgumentError("Invalid action passed to `execute_stack_action`.")

        if result:
            new_count += 1

    if new_count > 0:
        print(f"Created {new_count} new {action_description}Compose files.")
    else:
        print("Nothing to update.")

    print()
