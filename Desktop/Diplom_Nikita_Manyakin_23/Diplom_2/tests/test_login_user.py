import allure
import pytest
import requests
from data.urls import URL_AUTH_LOGIN
from data.messages import MSG_BAD_CREDENTIALS


class TestLoginUser:
    @allure.title("Логин под существующим пользователем")
    def test_login_existing_user_success(self, create_user):
        login_data = {
            "email": create_user["email"],
            "password": create_user["password"],
        }

        with allure.step("Отправка запроса на логин"):
            response = requests.post(URL_AUTH_LOGIN, json=login_data)

        with allure.step("Проверка успешного логина"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] is True
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
    def test_login_invalid_credentials_fails(self, invalid_data):
        with allure.step("Отправка запроса с неверными данными"):
            response = requests.post(URL_AUTH_LOGIN, json=invalid_data)

        with allure.step("Проверка ошибки авторизации"):
            assert response.status_code == 401
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data["message"] == MSG_BAD_CREDENTIALS
