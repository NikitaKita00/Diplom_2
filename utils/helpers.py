import random
import string


def generate_random_email():
    """Генерация случайного email"""
    username = ''.join(random.choices(string.ascii_lowercase, k=8))
    domain = ''.join(random.choices(string.ascii_lowercase, k=6))
    return f"{username}@{domain}.com"


def generate_random_name():
    """Генерация случайного имени"""
    first_name = ''.join(random.choices(string.ascii_letters, k=6))
    last_name = ''.join(random.choices(string.ascii_letters, k=8))
    return f"{first_name} {last_name}"


def get_auth_header(access_token):
    """Получение заголовка авторизации"""
    return {"Authorization": f"Bearer {access_token}"}