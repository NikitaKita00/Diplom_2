import allure
import requests
from utils.helpers import get_auth_header
from data.urls import URL_ORDERS
from data.messages import MSG_UNAUTHORISED


class TestUserOrders:
    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_user_orders_with_auth(self, create_user):
        headers = get_auth_header(create_user["access_token"])

        with allure.step("Запрос списка заказов пользователя"):
            response = requests.get(URL_ORDERS, headers=headers)

        with allure.step("Проверка успешного получения заказов"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] is True
            assert "orders" in response_data
            assert isinstance(response_data["orders"], list)

    @allure.title("Получение заказов неавторизованного пользователя")
    def test_get_user_orders_without_auth_fails(self):
        with allure.step("Запрос списка заказов без авторизации"):
            response = requests.get(URL_ORDERS)

        with allure.step("Проверка ошибки авторизации"):
            assert response.status_code == 401
            response_data = response.json()
            assert response_data["success"] is False
            assert response_data["message"] == MSG_UNAUTHORISED