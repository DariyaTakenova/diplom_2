import requests
import allure
from endpoints import ORDER

def create_order(ingredients, token=None):
    """Создаёт заказ через API и возвращает Response"""
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    with allure.step(f"Создание заказа с ингредиентами: {ingredients}"):
        response = requests.post(ORDER, json={"ingredients": ingredients}, headers=headers)
    return response
