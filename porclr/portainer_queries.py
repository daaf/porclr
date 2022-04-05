#!/usr/bin/env python3

# Third party imports
from urllib.error import HTTPError
import requests

# Standard library imports
import json


def get_auth_token(url: str, username: str, password: str):
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


def get_stack_list(url: str, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(f"http://{url}/api/stacks", headers=headers)
    response.raise_for_status()
    data = json.loads(response.text)
    stack_list = [{"id": stack["Id"], "name": stack["Name"]} for stack in data]

    return stack_list


def get_compose_file(url: str, stack_id: str, auth_token: str):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.get(f"http://{url}/api/stacks/{stack_id}/file", headers=headers)
    response.raise_for_status()
    data = json.loads(response.text)
    compose_file = data["StackFileContent"]
    return compose_file
