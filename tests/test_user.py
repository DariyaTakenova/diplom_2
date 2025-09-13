import requests
import pytest
from data import create_user, create_user_missing_field
from endpoints import REGISTER, LOGIN

def test_create_unique_user():
    user = create_user()
    response = requests.post(REGISTER, json=user)
    assert response.status_code == 200
    assert response.json()["success"] is True

def test_create_existing_user():
    user = create_user()
    requests.post(REGISTER, json=user)  # первый раз
    response = requests.post(REGISTER, json=user)  # второй раз
    assert response.status_code == 403  # пользователь уже существует

def test_create_user_missing_field():
    user = create_user_missing_field()
    response = requests.post(REGISTER, json=user)
    assert response.status_code == 400  # пропущено обязательное поле

def test_login_existing_user():
    user = create_user()
    requests.post(REGISTER, json=user)
    response = requests.post(LOGIN, json={"email": user["email"], "password": user["password"]})
    assert response.status_code == 200
    assert "accessToken" in response.json()

def test_login_invalid_credentials():
    response = requests.post(LOGIN, json={"email": "wrong@example.com", "password": "wrongpass"})
    assert response.status_code == 401