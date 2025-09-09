import allure
import pytest
import requests
from utils.helpers import generate_random_email, generate_random_name
from data.urls import URL_AUTH_REGISTER, URL_AUTH_USER
from data.messages import MSG_USER_EXISTS, MSG_REQUIRED_FIELDS


class TestCreateUser:
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user_success(self):
        user_data = {
            "email": generate_random_email(),
            "password": "password123",
            "name": generate_random_name(),
        }

        access_token = ""
        with allure.step("Отправка запроса на создание пользователя"):
            response = requests.post(URL_AUTH_REGISTER, json=user_data)

        try:
            with allure.step("Проверка статус кода и тела ответа"):
                assert response.status_code == 200
                response_data = response.json()
                assert response_data["success"] is True
                assert "accessToken" in response_data
                assert response_data["user"]["email"] == user_data["email"]
                assert response_data["user"]["name"] == user_data["name"]
                access_token = response_data.get("accessToken", "").replace(
                    "Bearer ", ""
                )
        finally:
            if access_token:
                try:
                    requests.delete(
                        URL_AUTH_USER,
                        headers={"Authorization": f"Bearer {access_token}"},
                    )
                except requests.RequestException:
                    pass

    @allure.title("Создание уже существующего пользователя")
    def test_create_existing_user_fails(self, create_user):
        duplicate_payload = {
            "email": create_user["email"],
            "password": create_user["password"],
            "name": create_user["name"],
        }

        with allure.step("Повторная отправка запроса с теми же данными"):
            response = requests.post(URL_AUTH_REGISTER, json=duplicate_payload)

        with allure.step("Проверка ошибки конфликта"):
            assert response.status_code == 403
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data["message"] == MSG_USER_EXISTS

    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field_fails(self, missing_field):
        invalid_data = {
            "email": generate_random_email(),
            "password": "password123",
            "name": generate_random_name(),
        }
        invalid_data.pop(missing_field)

        with allure.step("Отправка запроса с неполными данными"):
            response = requests.post(URL_AUTH_REGISTER, json=invalid_data)

        with allure.step("Проверка ошибки валидации"):
            assert response.status_code == 403
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data["message"] == MSG_REQUIRED_FIELDS
