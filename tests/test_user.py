import pytest
import allure
from helpers.user_helpers import register_user, login_user
from data import create_user


@allure.feature("Пользователи")
class TestUsers:

    @allure.title("Проверка обязательных полей при регистрации")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field(self, missing_field):
        """
        Попытка регистрации пользователя с пропущенным обязательным полем.
        Каждый обязательный атрибут проверяется отдельно.
        """
        user = create_user()
        user.pop(missing_field)

        with allure.step(f"Регистрация пользователя без поля: {missing_field}"):
            response = register_user(user)

        with allure.step("Проверка кода ошибки и сообщения"):
            assert response.status_code == 400
            body = response.json()
            assert "message" in body
            assert missing_field in body["message"] or "required" in body["message"].lower()
