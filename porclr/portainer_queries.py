#!/usr/bin/env python3

# Third party imports
import requests

# Standard library imports
import json


def get_auth_token(url: str, username: str, password: str):
    payload = {"username": username, "password": password}
    response = requests.post(f"http://{url}/api/auth", json=payload)
    response.raise_for_status()
    data = json.loads(response.text)
    auth_token = data["jwt"]

    return auth_token


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


# curl \
# -X POST http://127.0.0.1:9443/api/auth \
# -H "Content-Type: application/json" \
# -d '{"username": "admin", "password":"Practicedaily215!"}'


# curl \
#   -H "Authorization: Bearer \
#   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwidXNlcm5hbWUiOiJhZG1pbiIsInJvbGUiOjEsInNjb3BlIjoiZGVmYXVsdCIsImV4cCI6MTY0ODkzNTQ0OX0.M5ZMHkTmDaNZguMc8MFnROrLSX2AFlA55OHB5tABChE" \
#   http://127.0.0.1:9443/api/stacks
