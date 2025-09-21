import pytest
import requests
from endpoints import LOGIN, REGISTER
from data import create_user

@pytest.fixture(scope="session")
def test_user():
    """Создаём уникального тестового пользователя"""
    user = create_user()
    requests.post(REGISTER, json=user)  # игнорируем ошибки, если уже существует
    return user

@pytest.fixture(scope="session")
def auth_token(test_user):
    """Возвращает реальный токен авторизованного пользователя"""
    credentials = {"email": test_user["email"], "password": test_user["password"]}
    response = requests.post(LOGIN, json=credentials)
    assert response.status_code == 200, f"Не удалось авторизовать пользователя: {response.text}"
    token = response.json().get("accessToken")
    assert token is not None, "В ответе нет accessToken"
    return token
