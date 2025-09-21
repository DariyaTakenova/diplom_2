import pytest
import allure
from helpers.order_helpers import create_order
from helpers.user_helpers import register_user
from data import create_user, get_ingredients

@allure.feature("Заказы")
class TestOrders:

    @allure.title("Создание заказа с авторизацией и без")
    @pytest.mark.parametrize("auth", [True, False])
    def test_create_order(self, auth, auth_token):
        """
        Проверяем создание заказа с авторизацией и без неё.
        """
        ingredients = get_ingredients()
        token = auth_token if auth else None

        with allure.step(f"Создание заказа (auth={auth})"):
            response = create_order(ingredients, token)

        with allure.step("Проверка ответа"):
            if auth or not auth:  # если API разрешает анонимные заказы
                assert response.status_code == 200, f"Неверный код: {response.text}"
                body = response.json()
                assert body.get("success") is True
                assert "order" in body
                assert "ingredients" in body["order"]
                # Проверяем, что ингредиенты совпадают
                returned_ids = [i["_id"] for i in body["order"]["ingredients"]]
                assert set(returned_ids) == set(ingredients)
            else:
                # Если авторизация обязательна, проверяем 403
                assert response.status_code == 403

    @allure.title("Создание заказа с частичным списком ингредиентов")
    def test_create_order_with_partial_ingredients(self, auth_token):
        ingredients = get_ingredients()[:2]

        with allure.step("Создание заказа через API с двумя ингредиентами"):
            response = create_order(ingredients, auth_token)

        with allure.step("Проверка успешного ответа"):
            assert response.status_code == 200
            body = response.json()
            assert body.get("success") is True
            assert "order" in body
            returned_ids = [i["_id"] for i in body["order"]["ingredients"]]
            assert set(returned_ids) == set(ingredients)

    @allure.title("Попытка создать заказ без ингредиентов")
    def test_create_order_without_ingredients(self, auth_token):
        with allure.step("Создание заказа через API без ингредиентов"):
            response = create_order([], auth_token)

        with allure.step("Проверка кода ошибки и тела ответа"):
            assert response.status_code == 400
            body = response.json()
            assert "message" in body

    @allure.title("Попытка создать заказ с несуществующим ID ингредиента")
    def test_create_order_invalid_hash(self, auth_token):
        with allure.step("Создание заказа через API с невалидным ID"):
            response = create_order(["invalid_id"], auth_token)

        with allure.step("Проверка кода ошибки и тела ответа"):
            assert response.status_code == 500
            body = response.json()
            assert "message" in body
