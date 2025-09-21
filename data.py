import random
import string
import requests
from endpoints import INGREDIENTS

def random_string(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_user():
    """Возвращает уникального пользователя"""
    return {
        "email": f"{random_string()}@example.com",
        "password": random_string(),
        "name": f"User{random_string(3)}"
    }

def create_user_missing_field():
    """Возвращает пользователя без одного поля (для теста параметризации)"""
    user = create_user()
    user.pop("email")  # пример, поле удаляется в тесте
    return user

def get_ingredients():
    """Возвращает список всех ID ингредиентов"""
    response = requests.get(INGREDIENTS)
    return [item["_id"] for item in response.json()["data"]]
