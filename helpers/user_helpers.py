import requests
from data import URLS


def register_user(user: dict) -> requests.Response:

    return requests.post(URLS["register"], json=user)


def login_user(user: dict) -> requests.Response:

    return requests.post(URLS["login"], json={
        "email": user["email"],
        "password": user["password"]
    })


def delete_user(token: str) -> requests.Response:

    headers = {"Authorization": token}
    return requests.delete(URLS["user"], headers=headers)
