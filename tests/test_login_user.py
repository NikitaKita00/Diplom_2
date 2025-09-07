import allure
import pytest
import requests
from utils.helpers import get_auth_header


class TestLoginUser:
    @allure.title("Логин под существующим пользователем")
    def test_login_existing_user_success(self, base_url, create_user):
        """Тест успешного логина существующего пользователя"""
        login_data = {
            "email": create_user["email"],
            "password": create_user["password"],
        }

        with allure.step("Отправка запроса на логин"):
            response = requests.post(f"{base_url}/auth/login", json=login_data)

        with allure.step("Проверка успешного логина"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] == True
            assert "accessToken" in response_data
            assert response_data["user"]["email"] == create_user["email"]
            assert response_data["user"]["name"] == create_user["name"]

    @allure.title("Логин с неверными credentials")
    @pytest.mark.parametrize(
        "invalid_data",
        [
            {"email": "nonexistent@test.com", "password": "wrongpassword"},
            {"email": "invalid-email", "password": "password123"},
            {"email": "", "password": "password123"},
            {"email": "test@test.com", "password": ""},
        ],
    )
    def test_login_invalid_credentials_fails(self, base_url, invalid_data):
        """Тест логина с неверными учетными данными"""
        with allure.step("Отправка запроса с неверными данными"):
            response = requests.post(f"{base_url}/auth/login", json=invalid_data)

        with allure.step("Проверка ошибки авторизации"):
            assert response.status_code == 401
            response_data = response.json()
            assert response_data["success"] == False
            assert response_data["message"] == "email or password are incorrect"
