import random
import string
import requests

# Базовый URL API
BASE_URL = "https://stellarburgers.nomoreparties.site/api"

# Все используемые эндпоинты
URLS = {
    "register": f"{BASE_URL}/auth/register",
    "login": f"{BASE_URL}/auth/login",
    "user": f"{BASE_URL}/auth/user",
    "orders": f"{BASE_URL}/orders",
    "ingredients": f"{BASE_URL}/ingredients",
}


def generate_random_email() -> str:
    """Генерирует случайный email для регистрации."""
    return "test_" + "".join(random.choices(string.ascii_lowercase, k=6)) + "@yandex.ru"


def generate_random_password() -> str:
    """Генерирует случайный пароль."""
    return "".join(random.choices(string.ascii_letters + string.digits, k=10))


def create_user() -> dict:
    """Создаёт словарь с данными пользователя для регистрации."""
    return {
        "email": generate_random_email(),
        "password": generate_random_password(),
        "name": "TestUser"
    }


def get_ingredients() -> list[str]:
    """
    Получает список id ингредиентов через API.
    Возвращает список строк (id).
    """
    response = requests.get(URLS["ingredients"])
    response.raise_for_status()
    data = response.json()
    return [item["_id"] for item in data["data"]]
