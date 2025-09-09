import allure
import requests
from utils.helpers import get_auth_header
from data.urls import URL_ORDERS
from data.messages import MSG_INGREDIENT_IDS_REQUIRED


class TestCreateOrder:
    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth_and_ingredients(self, create_user, get_ingredients):
        headers = get_auth_header(create_user["access_token"])
        ingredients = [ingredient["_id"] for ingredient in get_ingredients[:2]]
        order_data = {"ingredients": ingredients}

        with allure.step("Создание заказа"):
            response = requests.post(URL_ORDERS, json=order_data, headers=headers)

        with allure.step("Проверка успешного создания заказа"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] is True
            assert "name" in response_data
            assert "order" in response_data
            assert "number" in response_data["order"]

    @allure.title("Создание заказа без авторизации с ингредиентами")
    def test_create_order_without_auth_with_ingredients(self, get_ingredients):
        ingredients = [ingredient["_id"] for ingredient in get_ingredients[:2]]
        order_data = {"ingredients": ingredients}

        with allure.step("Создание заказа без авторизации"):
            response = requests.post(URL_ORDERS, json=order_data)

        with allure.step("Проверка успешного создания заказа"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] is True

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients_fails(self, create_user):
        headers = get_auth_header(create_user["access_token"])
        order_data = {"ingredients": []}

        with allure.step("Создание заказа без ингредиентов"):
            response = requests.post(URL_ORDERS, json=order_data, headers=headers)

        with allure.step("Проверка ошибки валидации"):
            assert response.status_code == 400
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data["message"] == MSG_INGREDIENT_IDS_REQUIRED

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredient_hash_fails(self, create_user):
        headers = get_auth_header(create_user["access_token"])
        order_data = {"ingredients": ["invalid_hash_1", "invalid_hash_2"]}

        with allure.step("Создание заказа с невалидными ингредиентами"):
            response = requests.post(URL_ORDERS, json=order_data, headers=headers)

        with allure.step("Проверка внутренней ошибки сервера"):
            assert response.status_code == 500
