#!/usr/bin/env python3

# Standard library imports
import os

# Local imports
from porclr import portainer_queries, utils

STACKS = {
    "network-stack": ["duckdns", "pihole-unbound"],
    "grafana-stack": ["telegraf", "influxdb", "chronograf", "grafana"],
    "heimdall-stack": ["heimdall"],
    "home-stack": ["grocy"],
    "rss-stack": ["freshrss", "mariadb"],
    "test-stack": ["alpine"],
}

get_compose_attribute_value = utils.get_compose_attribute_value


def get_stack_name_from_app_name(app):
    """Search the STACKS dictionary for `app`. If `app` is found,
    return the name of the stack."""
    for stack in STACKS:
        if app in STACKS[stack]:
            return stack


def link_compose_file(path_to_original_compose_file, path_to_stack_dir):
    path_to_new_compose_file = f"{path_to_stack_dir}/docker-compose.yml"

    print(f"Checking for docker-compose.yml at {path_to_new_compose_file}...")

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


def copy_compose_file(path_to_stack_dir, url, stack_id, auth_token):
    path_to_new_compose_file = f"{path_to_stack_dir}/docker-compose.yml"

    print(f"Checking for docker-compose.yml at {path_to_new_compose_file}...")

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


def link_compose_files(portainer_compose_dir, linked_dir):
    """
    Iterate through the Docker Compose files in Portainer's data directory.
    For each Compose file, in a second directory, create a subdirectory with
    the same name as the stack. Inside the stack directory, create a link to the
    corresponding Compose file in Portainer's data directory.

    :param portainer_compose_dir: The path to the `compose` directory inside
        Portainer's data directory.
    :param linked_dir: The directory in which to create the links.
    """
    new_count = 0

    for subdir in os.listdir(portainer_compose_dir):
        path_to_original_compose_file = (
            f"{portainer_compose_dir}/{subdir}/docker-compose.yml"
        )
        app_name = get_compose_attribute_value(
            path_to_original_compose_file, "container_name"
        )
        stack_name = get_stack_name_from_app_name(app_name)
        path_to_stack_dir = f"{linked_dir}/{stack_name}"

        utils.create_dir_if_not_extant(path_to_stack_dir)

        result = link_compose_file(
            path_to_original_compose_file,
            path_to_stack_dir,
        )

        if result:
            new_count += 1

    if new_count > 1:
        print(f"Created {new_count} new links to Compose files.")
    elif new_count > 0:
        print(f"Created 1 new link to Compose file.")
    else:
        print("Nothing to update.")

    print()


def copy_compose_files(url: str, path: str, stack_list: list[dict], auth_token: str):
    new_count = 0

    for stack in stack_list:
        stack_id = stack["id"]
        stack_name = stack["name"]
        path_to_stack_dir = f"{path}/{stack_name}"

        utils.create_dir_if_not_extant(path_to_stack_dir)
        result = copy_compose_file(
            path_to_stack_dir, url, stack_id, auth_token=auth_token
        )

        if result:
            new_count += 1

    if new_count > 1:
        print(f"Created {new_count} new Compose files.")
    elif new_count > 0:
        print(f"Created 1 new Compose file.")
    else:
        print("Nothing to update.")

    print()
