import pytest
import allure
from data import create_user
from helpers.user_helpers import register_user, login_user


@pytest.fixture
def new_user():
    """
    Фикстура для генерации нового пользователя (случайные данные).
    """
    return create_user()


@pytest.fixture
def auth_token(new_user):
    """
    Фикстура для регистрации и получения токена авторизации.
    """
    with allure.step("Регистрация нового пользователя и получение токена"):
        response = register_user(new_user)
        assert response.status_code == 200, f"Ошибка регистрации: {response.text}"
        body = response.json()
        token = body.get("accessToken")
        assert token, f"Токен не получен: {body}"
        return token
