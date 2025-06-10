import requests
import allure
from urls import Urls, Handlers
from  config import headers_auth_json
from data import GetOrdersResponses


@allure.suite("Получение заказов конкретного пользователя")
class TestGetUserOrders:

    @allure.title("Получение заказов авторизованным пользователем")
    def test_get_orders_authorized(self, user_for_test):
        _, access_token = user_for_test
        headers = headers_auth_json(access_token)

        with allure.step("Отправка GET-запроса на получение заказов авторизованным пользователем"):
            response = requests.get(Urls.MAIN_URL + Handlers.GET_ORDERS, headers=headers)

        with allure.step("Проверка кода ответа"):
            assert response.status_code == GetOrdersResponses.authorized_success["status_code"]

        with allure.step("Проверка тела ответа"):
            body = response.json()
            assert body.get("success") is GetOrdersResponses.authorized_success["body"]["success"]
            assert isinstance(body.get("orders"), GetOrdersResponses.authorized_success["body"]["orders_type"])

    @allure.title("Получение заказов неавторизованным пользователем")
    def test_get_orders_unauthorized(self):
        with allure.step("Отправка GET-запроса на получение заказов неавторизованным пользователем"):
            response = requests.get(Urls.MAIN_URL + Handlers.GET_ORDERS)

        with allure.step("Проверка кода ответа"):
            assert response.status_code == GetOrdersResponses.unauthorized_error["status_code"]

        with allure.step("Проверка тела ответа"):
            body = response.json()
            assert body.get("success") is GetOrdersResponses.unauthorized_error["body"]["success"]
            assert body.get("message") == GetOrdersResponses.unauthorized_error["body"]["message"]