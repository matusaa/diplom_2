import requests
import allure
from config import Urls, Handlers

@allure.suite("Получение заказов конкретного пользователя")
class TestGetUserOrders:

    @allure.title("Получение заказов авторизованным пользователем")
    def test_get_orders_authorized(self, user_for_test):
        _, access_token = user_for_test
        headers = Handlers.headers_auth_json(access_token)
        response = requests.get(Urls.MAIN_URL + Handlers.GET_ORDERS, headers=headers)
        assert response.status_code == 200
        body = response.json()
        assert body.get("success") is True
        assert isinstance(body.get("orders"), list)

    @allure.title("Получение заказов неавторизованным пользователем")
    def test_get_orders_unauthorized(self):
        response = requests.get(Urls.MAIN_URL + Handlers.GET_ORDERS)
        assert response.status_code == 401
        body = response.json()
        assert body.get("success") is False
        assert body.get("message") == "You should be authorised"