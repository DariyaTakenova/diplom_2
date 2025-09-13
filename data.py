import random
import string

def random_email():
    """Генерирует уникальный email для каждого пользователя"""
    return f"test_{''.join(random.choices(string.ascii_lowercase, k=5))}@example.com"

def create_user(name="Test User", password="12345678", email=None):
    return {
        "email": email or random_email(),
        "password": password,
        "name": name
    }

def create_user_missing_field():
    return {
        "email": random_email(),
        "password": "12345678"
        # поле name пропущено
    }