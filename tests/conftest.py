import pytest
import requests
from utils.helpers import generate_random_email, generate_random_name


@pytest.fixture
def base_url():
    return "https://stellarburgers.nomoreparties.site/api"


@pytest.fixture
def user_data():
    """Генерация тестовых данных пользователя"""
    return {
        "email": generate_random_email(),
        "password": "password123",
        "name": generate_random_name()
    }


@pytest.fixture
def create_user(base_url, user_data):
    """Создание пользователя и возврат данных"""
    response = requests.post(f"{base_url}/auth/register", json=user_data)
    assert response.status_code == 200
    user_data["access_token"] = response.json().get("accessToken", "").replace("Bearer ", "")
    return user_data


@pytest.fixture
def get_ingredients(base_url):
    """Получение списка ингредиентов"""
    response = requests.get(f"{base_url}/ingredients")
    assert response.status_code == 200
    return response.json()["data"]