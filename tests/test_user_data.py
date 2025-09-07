import allure
import pytest
import requests
from utils.helpers import get_auth_header, generate_random_email, generate_random_name


class TestUserData:
    @allure.title("Изменение данных пользователя с авторизацией")
    def test_update_user_data_with_auth_success(self, base_url, create_user):
        """Тест успешного изменения данных пользователя с авторизацией"""
        new_data = {
            "email": generate_random_email(),
            "name": generate_random_name(),
            "password": "newpassword123",
        }

        headers = get_auth_header(create_user["access_token"])

        with allure.step("Отправка запроса на обновление данных"):
            response = requests.patch(
                f"{base_url}/auth/user", json=new_data, headers=headers
            )

        with allure.step("Проверка успешного обновления"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] == True
            assert response_data["user"]["email"] == new_data["email"]
            assert response_data["user"]["name"] == new_data["name"]

    @allure.title("Изменение данных пользователя без авторизации")
    def test_update_user_data_without_auth_fails(self, base_url, create_user):
        """Тест изменения данных пользователя без авторизации"""
        new_data = {"email": generate_random_email(), "name": generate_random_name()}

        with allure.step("Отправка запроса без авторизации"):
            response = requests.patch(f"{base_url}/auth/user", json=new_data)

        with allure.step("Проверка ошибки авторизации"):
            assert response.status_code == 401
            response_data = response.json()
            assert response_data["success"] == False
            assert response_data["message"] == "You should be authorised"

    @allure.title("Изменение отдельных полей пользователя")
    @pytest.mark.parametrize("field_to_update", ["email", "name", "password"])
    def test_update_single_field_with_auth(
        self, base_url, create_user, field_to_update
    ):
        """Тест изменения отдельных полей пользователя"""
        update_data = {}
        if field_to_update == "email":
            update_data["email"] = generate_random_email()
        elif field_to_update == "name":
            update_data["name"] = generate_random_name()
        elif field_to_update == "password":
            update_data["password"] = "newpassword123"

        headers = get_auth_header(create_user["access_token"])

        with allure.step(f"Обновление поля: {field_to_update}"):
            response = requests.patch(
                f"{base_url}/auth/user", json=update_data, headers=headers
            )

        with allure.step("Проверка успешного обновления"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] == True

            if field_to_update in ["email", "name"]:
                assert (
                    response_data["user"][field_to_update]
                    == update_data[field_to_update]
                )
