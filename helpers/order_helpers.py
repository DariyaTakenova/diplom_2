import requests
from data import URLS


def create_order(ingredients: list[str], token: str | None = None) -> requests.Response:

    headers = {}
    if token:
        headers["Authorization"] = token

    payload = {"ingredients": ingredients}

    return requests.post(URLS["orders"], json=payload, headers=headers)


def get_ingredients_list() -> requests.Response:

    return requests.get(URLS["ingredients"])
