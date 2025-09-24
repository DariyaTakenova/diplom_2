import pytest
import allure
from helpers.user_helpers import register_user
from data import create_user


@allure.feature("Регистрация пользователя")
class TestUsers:

    @allure.story("Регистрация без email")
    @allure.title("Регистрация без email")
    def test_create_user_without_email(self):
        user = create_user()
        user.pop("email")

        with allure.step("Регистрация пользователя без email"):
            response = register_user(user)

        with allure.step("Проверка ошибки"):
            assert response.status_code == 403, f"Неверный код: {response.text}"
            body = response.json()
            assert body.get("success") is False
            assert body.get("message") == "Email, password and name are required fields"

    @allure.story("Регистрация без пароля")
    @allure.title("Регистрация без password")
    def test_create_user_without_password(self):
        user = create_user()
        user.pop("password")

        with allure.step("Регистрация пользователя без password"):
            response = register_user(user)

        with allure.step("Проверка ошибки"):
            assert response.status_code == 403, f"Неверный код: {response.text}"
            body = response.json()
            assert body.get("success") is False
            assert body.get("message") == "Email, password and name are required fields"

    @allure.story("Регистрация без имени")
    @allure.title("Регистрация без name")
    def test_create_user_without_name(self):
        user = create_user()
        user.pop("name")

        with allure.step("Регистрация пользователя без name"):
            response = register_user(user)

        with allure.step("Проверка ошибки"):
            assert response.status_code == 403, f"Неверный код: {response.text}"
            body = response.json()
            assert body.get("success") is False
            assert body.get("message") == "Email, password and name are required fields"
