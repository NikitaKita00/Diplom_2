import allure
import requests
from utils.helpers import get_auth_header, generate_random_email, generate_random_name
from data.urls import URL_AUTH_USER
from data.messages import MSG_UNAUTHORISED


class TestUserData:
    @allure.title("Изменение данных пользователя с авторизацией (все поля)")
    def test_update_user_data_with_auth_success(self, create_user):
        new_data = {
            "email": generate_random_email(),
            "name": generate_random_name(),
            "password": "newpassword123",
        }
        headers = get_auth_header(create_user["access_token"])

        with allure.step("Отправка запроса на обновление данных (все поля)"):
            response = requests.patch(URL_AUTH_USER, json=new_data, headers=headers)

        with allure.step("Проверка успешного обновления"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] is True
            assert response_data["user"]["email"] == new_data["email"]
            assert response_data["user"]["name"] == new_data["name"]

    @allure.title("Изменение данных пользователя без авторизации")
    def test_update_user_data_without_auth_fails(self):
        new_data = {
            "email": generate_random_email(),
            "name": generate_random_name(),
        }

        with allure.step("Отправка запроса без авторизации"):
            response = requests.patch(URL_AUTH_USER, json=new_data)

        with allure.step("Проверка ошибки авторизации"):
            assert response.status_code == 401
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data["message"] == MSG_UNAUTHORISED

    @allure.title("Изменение email с авторизацией")
    def test_update_email_with_auth_success(self, create_user):
        headers = get_auth_header(create_user["access_token"])
        payload = {"email": generate_random_email()}

        with allure.step("Обновление email"):
            response = requests.patch(URL_AUTH_USER, json=payload, headers=headers)

        with allure.step("Проверка успешного обновления email"):
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["user"]["email"] == payload["email"]

    @allure.title("Изменение name с авторизацией")
    def test_update_name_with_auth_success(self, create_user):
        headers = get_auth_header(create_user["access_token"])
        payload = {"name": generate_random_name()}

        with allure.step("Обновление name"):
            response = requests.patch(URL_AUTH_USER, json=payload, headers=headers)

        with allure.step("Проверка успешного обновления name"):
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["user"]["name"] == payload["name"]

    @allure.title("Изменение password с авторизацией")
    def test_update_password_with_auth_success(self, create_user):
        headers = get_auth_header(create_user["access_token"])
        payload = {"password": "newpassword123"}

        with allure.step("Обновление password"):
            response = requests.patch(URL_AUTH_USER, json=payload, headers=headers)

        with allure.step("Проверка успешного обновления password"):
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
