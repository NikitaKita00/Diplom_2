import allure
import pytest
import requests


class TestCreateUser:
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user_success(self, base_url, user_data):
        """Тест успешного создания уникального пользователя"""
        with allure.step("Отправка запроса на создание пользователя"):
            response = requests.post(f"{base_url}/auth/register", json=user_data)

        with allure.step("Проверка статус кода и тела ответа"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] == True
            assert "accessToken" in response_data
            assert response_data["user"]["email"] == user_data["email"]
            assert response_data["user"]["name"] == user_data["name"]

    @allure.title("Создание уже существующего пользователя")
    def test_create_existing_user_fails(self, base_url, create_user):
        """Тест попытки создания уже существующего пользователя"""
        with allure.step("Повторная отправка запроса с теми же данными"):
            response = requests.post(f"{base_url}/auth/register", json=create_user)

        with allure.step("Проверка ошибки конфликта"):
            assert response.status_code == 403
            response_data = response.json()
            assert response_data["success"] == False
            assert response_data["message"] == "User already exists"

    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field_fails(self, base_url, user_data, missing_field):
        """Тест создания пользователя без обязательного поля"""
        with allure.step(f"Удаление обязательного поля: {missing_field}"):
            invalid_data = user_data.copy()
            invalid_data.pop(missing_field)

        with allure.step("Отправка запроса с неполными данными"):
            response = requests.post(f"{base_url}/auth/register", json=invalid_data)

        with allure.step("Проверка ошибки валидации"):
            assert response.status_code == 403
            response_data = response.json()
            assert response_data["success"] == False
            assert (
                response_data["message"]
                == "Email, password and name are required fields"
            )
