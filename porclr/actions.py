#!/usr/bin/env python3

# Third party imports
from decouple import config
from typer import echo

# Standard library imports
import os

# Local imports
from porclr import portainer_queries
from porclr import utils


class Action:

    url = config("PORTAINER_URL")
    auth_token = ""

    def __init__(self, username, password: str) -> None:
        self.auth_token = portainer_queries.get_auth_token(self.url, username, password)


class ComposeFileAction(Action):

    stack_list = None
    local_path = None

    def __init__(self, path: str, username, password: str) -> None:
        super().__init__(username, password)
        self.stack_list = portainer_queries.get_stack_list(self.url, self.auth_token)
        self.local_path = path if path else config("LOCAL_REPO")

    def _create_stack_dir(self, stack_name):
        path_to_stack_dir = f"{self.local_path}/{stack_name}"
        utils.create_dir_if_not_extant(path_to_stack_dir)
        return path_to_stack_dir

    def _execute(self, func, stack_name, *args, **kwargs):
        path_to_stack_dir = self._create_stack_dir(stack_name)
        path_to_new_compose_file = f"{path_to_stack_dir}/docker-compose.yml"
        result = func(path_to_new_compose_file, *args, **kwargs)

        return result


class Link(ComposeFileAction):
    def __init__(self, path: str, username: str, password: str) -> None:
        super().__init__(path, username, password)
        self.portainer_compose_dir = config("PORTAINER_COMPOSE_DIR")

    def execute(self):
        new_count = 0

        for stack in self.stack_list:
            stack_id = stack["id"]
            stack_name = stack["name"]
            path_to_original_compose_file = (
                f"{self.portainer_compose_dir}/{stack_id}/docker-compose.yml"
            )
            result = self._execute(
                self._link_compose_file, stack_name, path_to_original_compose_file
            )

            if result:
                new_count += 1
        
        echo(f"Linked {new_count} Compose files.\n")

    def _link_compose_file(
        self, path_to_new_compose_file, path_to_original_compose_file
    ):
        if not os.path.exists(path_to_new_compose_file):
            os.link(path_to_original_compose_file, path_to_new_compose_file)

            echo(
                f"\tCreated link to {path_to_original_compose_file} in {path_to_new_compose_file}.\n"
            )
            return True

        echo(f"\t{path_to_new_compose_file} already exists.\n")
        return False


class Copy(ComposeFileAction):
    def __init__(self, path: str, username: str, password: str) -> None:
        super().__init__(path, username, password)

    def execute(self):
        new_count = 0

        for stack in self.stack_list:
            stack_id = stack["id"]
            stack_name = stack["name"]

            result = self._execute(self._copy_compose_file, stack_name, stack_id)

            if result:
                new_count += 1
        
        echo(f"Copied {new_count} Compose files.\n")

    def _copy_compose_file(self, path_to_new_compose_file, stack_id):
        if not os.path.exists(path_to_new_compose_file):
            compose_file = portainer_queries.get_compose_file(
                self.url, stack_id, self.auth_token
            )
            with open(path_to_new_compose_file, "w") as file:
                file.write(compose_file)

            echo(f"\tCopied docker-compose.yml to {path_to_new_compose_file}.\n")
            return True

        echo(f"\t{path_to_new_compose_file} already exists.\n")
        return False
