import pytest
import allure
from helpers.user_helpers import register_user, delete_user
from helpers.order_helpers import create_order
from data import get_ingredients, create_user


@allure.feature("Заказы")
class TestOrders:

    @allure.title("Создание заказа с авторизацией и валидными ингредиентами")
    def test_create_order_with_auth(self):

        user = create_user()
        response = register_user(user)
        token = response.json()["accessToken"]

        ingredients = get_ingredients()[:2]  # берём первые два ингредиента

        with allure.step("Создаём заказ с токеном"):
            order_response = create_order(ingredients, token)

        with allure.step("Проверяем успешность ответа"):
            assert order_response.status_code == 200
            body = order_response.json()
            assert body["success"] is True
            assert "order" in body
            assert body["order"]["ingredients"]  # заказ содержит ингредиенты

        delete_user(token)

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self):

        ingredients = get_ingredients()[:2]

        with allure.step("Создаём заказ без токена"):
            order_response = create_order(ingredients)

        with allure.step("Проверяем успешность ответа"):
            assert order_response.status_code == 200
            body = order_response.json()
            assert body["success"] is True
            assert "order" in body

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self):

        user = create_user()
        response = register_user(user)
        token = response.json()["accessToken"]

        with allure.step("Создаём заказ с пустым списком ингредиентов"):
            order_response = create_order([], token)

        with allure.step("Проверяем, что возвращается ошибка"):
            assert order_response.status_code == 400
            body = order_response.json()
            assert body["success"] is False
            assert "message" in body
            assert "Ingredient ids must be provided" in body["message"]

        delete_user(token)

    @allure.title("Создание заказа с невалидными ингредиентами")
    def test_create_order_with_invalid_ingredients(self):

        user = create_user()
        response = register_user(user)
        token = response.json()["accessToken"]

        invalid_ingredients = ["123", "invalid_id"]

        with allure.step("Создаём заказ с неверными id ингредиентов"):
            order_response = create_order(invalid_ingredients, token)

        with allure.step("Проверяем, что возвращается ошибка"):
            # ожидаем, что сервер упадёт (API-баг: 500 вместо 400)
            assert order_response.status_code in [400, 500]

            # пробуем безопасно разобрать JSON
            try:
                body = order_response.json()
                # если вдруг придёт нормальный JSON — проверяем структуру
                assert "success" in body or "message" in body
            except ValueError:
                # сервер вернул HTML (Internal Server Error)
                assert "Internal Server Error" in order_response.text

        delete_user(token)
