import requests
import allure
from endpoints import REGISTER, LOGIN

def register_user(user):
    """Регистрация пользователя через API"""
    with allure.step(f"Регистрация пользователя с данными: {user}"):
        response = requests.post(REGISTER, json=user)
    return response

def login_user(email, password):
    """Авторизация пользователя через API"""
    with allure.step(f"Авторизация пользователя с email: {email}"):
        response = requests.post(LOGIN, json={"email": email, "password": password})
    return response
