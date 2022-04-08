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
    """Represents the base set of attributes for an action that can be
    performed with the Portainer API."""

    url: str = config("PORTAINER_URL")
    """The URL of the Portainer instance to perform the action on.
    Retrieved from the `PORTAINER_URL` environment variable defined
    in /.env."""
    auth_token: str = ""
    """The JWT that will be used to authenticate with Portainer."""

    def __init__(self, username: str, password: str) -> None:
        """
        Gets the JWT that will be used to authenticate with Portainer and
        assigns it to the `auth_token` class variable for use by child classes.

        :param username: The username to use to authenticate with Portainer.
        :param password: The password to use to authenticate with Portainer.
        """
        self.auth_token = portainer_queries.get_auth_token(self.url, username, password)


class ComposeFileAction(Action):
    """Represents an action that is executed for all stacks in the Portainer
    instance."""

    stack_list: list[dict] = None
    """A list of stack IDs and names from the Portainer instance."""
    local_path: str = None
    """The path to the directory where the Compose files should be 
    linked or copied and the associated subdirectories should be created."""

    def __init__(self, path: str, username: str, password: str) -> None:
        """
        Gets `stack_list` and `local_path` and authenticates with Portainer.

        :param path: The path at which to create the links or copies and
            associated subdirectories.
        :param username: The username to use to authenticate with Portainer.
        :param password: The password to use to authenticate with Portainer.
        """
        super().__init__(username, password)
        self.stack_list = portainer_queries.get_stack_list(self.url, self.auth_token)
        self.local_path = path if path else config("LOCAL_REPO")

    def _create_stack_dir(self, stack_name: str) -> str:
        """
        Creates a subdirectory of `local_path` with the same name as a
        Portainer stack.

        :param stack_name: The name of the stack for which to create a directory.
        :return: The path to the newly created stack directory.
        """
        path_to_stack_dir = f"{self.local_path}/{stack_name}"
        utils.create_dir_if_not_extant(path_to_stack_dir)
        return path_to_stack_dir

    def _execute(self, child_class: "ComposeFileAction", func: function):
        """
        Iterates through all Portainer stacks, creates the required
        directories on the local filesystem, and executes the function
        specified in `func`.

        :param child_class: The type of the object that is calling the `_execute`
        method, which should be a child class of `ComposeFileAction`.
        :param func: The function that should be executed for each stack.
        """
        new_count = 0

        for stack in self.stack_list:
            stack_id = stack["id"]
            stack_name = stack["name"]

            path_to_stack_dir = self._create_stack_dir(stack_name)
            path_to_new_compose_file = f"{path_to_stack_dir}/docker-compose.yml"

            result = func(path_to_new_compose_file, stack_id)
            result_type = type(child_class).__name__.lower()

            if result:
                new_count += 1

        if result:
            echo(f"Created {result_type} for {new_count} Compose files.\n")
        else:
            echo("Nothing to update.")


class Link(ComposeFileAction):
    """Represents an action that creates hard links to the Compose files in a local
    Portainer volume."""

    def __init__(self, path: str, username: str, password: str) -> None:
        """Gets the path to the `compose` directory within the local Portainer
        volume, gets `stack_list` and `local_path`, and authenticates with
        Portainer.

        :param path: The path at which to create the links or copies and
            associated subdirectories.
        :param username: The username to use to authenticate with Portainer.
        :param password: The password to use to authenticate with Portainer.
        """
        super().__init__(path, username, password)
        self.portainer_compose_dir = config("PORTAINER_COMPOSE_DIR")

    def execute(self):
        """Passes `_link_compose_file` to parent `_execute` method so that
        `_link_compose_file` is executed for every stack in the Portainer
        instance."""
        self._execute(self, self._link_compose_file)

    def _link_compose_file(self, path_to_new_compose_file: str, stack_id: str) -> bool:
        """Creates a hard link to a Compose file in a local Portainer
        volume.

        :param path_to_new_compose_file: The path to the location where the link
            to the Compose file should be created.
        :param stack_id: The `id` of the stack to link Compose file for.
        :return: If a link is created, returns True. If a docker-compose.yml
        already exists at the specified location, returns False.
        """
        path_to_original_compose_file = (
            f"{self.portainer_compose_dir}/{stack_id}/docker-compose.yml"
        )
        if not os.path.exists(path_to_new_compose_file):
            os.link(path_to_original_compose_file, path_to_new_compose_file)

            echo(
                f"\tCreated link to {path_to_original_compose_file} in {path_to_new_compose_file}.\n"
            )
            return True

        echo(f"\t{path_to_new_compose_file} already exists.\n")
        return False


class Copy(ComposeFileAction):
    """Represents an action that copies the Docker Compose files for all stacks
    in the Portainer instance."""

    def __init__(self, path: str, username: str, password: str) -> None:
        """Gets `stack_list` and `local_path` and authenticates with Portainer.

        :param path: The path at which to create the links or copies and
            associated subdirectories.
        :param username: The username to use to authenticate with Portainer.
        :param password: The password to use to authenticate with Portainer.
        """
        super().__init__(path, username, password)

    def execute(self) -> None:
        """Passes `_copy_compose_file` to parent `_execute` method so that
        `_copy_compose_file` is executed for every stack in the Portainer
        instance."""
        self._execute(self, self._copy_compose_file)

    def _copy_compose_file(self, path_to_new_compose_file, stack_id) -> bool:
        """Creates a copy of a specified Compose file from Portainer.

        :param path_to_new_compose_file: The path to the location where the copy
            of the Compose file should be created.
        :param stack_id: The `id` of the stack to copy Compose file for.
        :return: If a copy is created, returns True. If a docker-compose.yml
        already exists at the specified location, returns False.
        """
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
