import pytest
import allure
from helpers.user_helpers import register_user, login_user
from data import create_user


@allure.feature("Логин пользователя")
class TestUserLogin:

    @allure.story("Успешный логин")
    @allure.title("Логин с корректными данными")
    def test_login_successful(self):
        user = create_user()
        register_user(user)

        with allure.step("Авторизация с корректными данными"):
            response = login_user(user)

        with allure.step("Проверка успешного ответа"):
            assert response.status_code == 200, f"Ошибка: {response.text}"
            body = response.json()
            assert body.get("success") is True
            assert "accessToken" in body

    @allure.story("Логин с неверным паролем")
    @allure.title("Логин с неверным password")
    def test_login_with_invalid_password(self):
        user = create_user()
        register_user(user)
        user["password"] = "wrong_password"

        with allure.step("Авторизация с неверным паролем"):
            response = login_user(user)

        with allure.step("Проверка ошибки"):
            assert response.status_code == 401, f"Неверный код: {response.text}"
            body = response.json()
            assert body.get("success") is False
            assert body.get("message") == "email or password are incorrect"

    @allure.story("Логин с неверным email")
    @allure.title("Логин с неверным email")
    def test_login_with_invalid_email(self):
        user = create_user()
        register_user(user)
        user["email"] = "invalid@example.com"

        with allure.step("Авторизация с неверным email"):
            response = login_user(user)

        with allure.step("Проверка ошибки"):
            assert response.status_code == 401, f"Неверный код: {response.text}"
            body = response.json()
            assert body.get("success") is False
            assert body.get("message") == "email or password are incorrect"
