import requests
import pytest
from endpoints import ORDER, INGREDIENTS

def get_ingredients():
    response = requests.get(INGREDIENTS)
    return [item["_id"] for item in response.json()["data"]]

def test_create_order_with_auth(auth_token):
    ingredients = get_ingredients()
    response = requests.post(ORDER, json={"ingredients": ingredients},
                             headers={"Authorization": auth_token})
    assert response.status_code == 200
    assert response.json()["success"] is True

def test_create_order_without_auth():
    ingredients = get_ingredients()
    response = requests.post(ORDER, json={"ingredients": ingredients})
    # API разрешает анонимные заказы, поэтому проверяем 200
    assert response.status_code == 200
    assert response.json()["success"] is True

def test_create_order_with_ingredients(auth_token):
    ingredients = get_ingredients()[:2]
    response = requests.post(ORDER, json={"ingredients": ingredients},
                             headers={"Authorization": auth_token})
    assert response.status_code == 200
    assert response.json()["success"] is True

def test_create_order_without_ingredients(auth_token):
    response = requests.post(ORDER, json={"ingredients": []},
                             headers={"Authorization": auth_token})
    assert response.status_code == 400

def test_create_order_invalid_hash(auth_token):
    response = requests.post(ORDER, json={"ingredients": ["invalid_id"]},
                             headers={"Authorization": auth_token})
    assert response.status_code == 500