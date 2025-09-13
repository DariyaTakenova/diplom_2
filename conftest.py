import pytest
import requests
from data import create_user
from endpoints import LOGIN, REGISTER

@pytest.fixture(scope="session")
def auth_token():
    """Регистрируем уникального пользователя для получения токена один раз на сессию"""
    user = create_user()
    requests.post(REGISTER, json=user)
    response = requests.post(LOGIN, json={"email": user["email"], "password": user["password"]})
    return response.json().get("accessToken")