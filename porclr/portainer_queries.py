#!/usr/bin/env python3

# Third party imports
import requests

# Standard library imports
import json


def get_auth_token(url: str, username: str, password: str) -> str:
    """
    Gets a JSON Web Token (JWT) to use to authenticate with Portainer.

    :param url: The URL of the Portainer instance, including port number.
        For example, 127.0.0.1:9443.
    :param username: The username to use to authenticate with Portainer.
    :param password: The password to use to authenticate with Portainer.
    :returns: If the user-provided credentials are valid, a JWT token.
    """
    headers = {"Content-Type": "application/json"}
    payload = {"username": username, "password": password}

    try:
        response = requests.post(
            f"http://{url}/api/auth",
            headers=headers,
            json=(payload),
        )
        data = json.loads(response.text)
        auth_token = data["jwt"]

        return auth_token
    except:
        print("Incorrect password")


def get_stack_list(url: str, auth_token: str) -> list[dict]:
    """
    Gets a list of stack IDs and names from a Portainer instance.

    :param url: The URL of the Portainer instance, including port number.
        For example, 127.0.0.1:9443.
    :param auth_token: The JSON Web Token (JWT) to use to authenticate
        with Portainer.
    :returns: A list of dicts, where each dict contains the ID and name
        of a stack in Portainer.
    """
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(f"http://{url}/api/stacks", headers=headers)
    response.raise_for_status()
    data = json.loads(response.text)
    stack_list = [{"id": stack["Id"], "name": stack["Name"]} for stack in data]

    return stack_list


def get_compose_file(url: str, stack_id: str, auth_token: str) -> str:
    """
    Gets the contents of a Docker Compose file from a Portainer instance.

    :param url: The URL of the Portainer instance, including port number.
        For example, 127.0.0.1:9443.
    :param stack_id: The ID number of the Portainer stack for which to
        retrieve the Compose file.
    :param auth_token: The JSON Web Token (JWT) to use to authenticate
        with Portainer.
    :returns: The contents of the requested Compose file.
    """
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(f"http://{url}/api/stacks/{stack_id}/file", headers=headers)
    response.raise_for_status()
    data = json.loads(response.text)
    compose_file = data["StackFileContent"]
    return compose_file
