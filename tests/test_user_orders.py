import allure
import pytest
import requests
from utils.helpers import get_auth_header


class TestUserOrders:
    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_user_orders_with_auth(self, base_url, create_user):
        """Тест получения заказов авторизованного пользователя"""
        headers = get_auth_header(create_user["access_token"])

        with allure.step("Запрос списка заказов пользователя"):
            response = requests.get(f"{base_url}/orders", headers=headers)

        with allure.step("Проверка успешного получения заказов"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] == True
            assert "orders" in response_data
            assert isinstance(response_data["orders"], list)

    @allure.title("Получение заказов неавторизованного пользователя")
    def test_get_user_orders_without_auth_fails(self, base_url):
        """Тест получения заказов без авторизации"""
        with allure.step("Запрос списка заказов без авторизации"):
            response = requests.get(f"{base_url}/orders")

        with allure.step("Проверка ошибки авторизации"):
            assert response.status_code == 401
            response_data = response.json()
            assert response_data["success"] == False
            assert response_data["message"] == "You should be authorised"
