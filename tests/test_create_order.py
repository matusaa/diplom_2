import allure
import requests
from urls import Urls, Handlers
from config import headers_auth_json
from helpers import Helper


from data import OrderData, OrderResponses

@allure.suite("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и валидными ингредиентами")
    def test_create_order_with_valid_ingredients(self, user_for_test):
        _, access_token = user_for_test
        ingredients = Helper.get_ingredients_ids()[:2]
        payload = OrderData.valid_ingredients_payload(ingredients)
        headers = headers_auth_json(access_token)

        with allure.step("Отправка POST-запроса на создание заказа с авторизацией"):
            response = requests.post(Urls.MAIN_URL + Handlers.MAKE_ORDER, headers=headers, json=payload)

        with allure.step("Проверка кода ответа"):
            assert response.status_code == OrderResponses.success["status_code"]

        with allure.step("Проверка тела ответа"):
            body = response.json()
            assert body.get("success") is OrderResponses.success["body"]["success"]

    @allure.title("Создание заказа без авторизации и валидными ингредиентами")
    def test_create_order_without_auth(self):
        ingredients = Helper.get_ingredients_ids()[:2]
        payload = OrderData.valid_ingredients_payload(ingredients)

        with allure.step("Отправка POST-запроса на создание заказа без авторизации"):
            response = requests.post(Urls.MAIN_URL + Handlers.MAKE_ORDER, json=payload)

        with allure.step("Проверка кода ответа"):
            assert response.status_code == OrderResponses.success["status_code"]

        with allure.step("Проверка тела ответа"):
            body = response.json()
            assert body.get("success") is OrderResponses.success["body"]["success"]

    @allure.title("Создание заказа с авторизацией и без ингредиентов")
    def test_create_order_with_auth_without_ingredients(self, user_for_test):
        _, access_token = user_for_test
        payload = OrderData.empty_ingredients_payload
        headers = headers_auth_json(access_token)

        with allure.step("Отправка POST-запроса на создание заказа с авторизацией и пустым списком ингредиентов"):
            response = requests.post(Urls.MAIN_URL + Handlers.MAKE_ORDER, headers=headers, json=payload)

        with allure.step("Проверка кода ответа"):
            assert response.status_code == OrderResponses.missing_ingredients["status_code"]

        with allure.step("Проверка тела ответа"):
            body = response.json()
            assert body.get("success") is OrderResponses.missing_ingredients["body"]["success"]
            assert body.get("message") == OrderResponses.missing_ingredients["body"]["message"]

    @allure.title("Создание заказа без авторизации и без ингредиентов")
    def test_create_order_without_auth_without_ingredients(self):
        payload = OrderData.empty_ingredients_payload

        with allure.step("Отправка POST-запроса на создание заказа без авторизации и пустым списком ингредиентов"):
            response = requests.post(Urls.MAIN_URL + Handlers.MAKE_ORDER, json=payload)

        with allure.step("Проверка кода ответа"):
            assert response.status_code == OrderResponses.missing_ingredients["status_code"]

        with allure.step("Проверка тела ответа"):
            body = response.json()
            assert body.get("success") is OrderResponses.missing_ingredients["body"]["success"]
            assert body.get("message") == OrderResponses.missing_ingredients["body"]["message"]

    @allure.title("Создание заказа c неверным хешем ингредиентов")
    def test_create_order_with_auth_invalid_ingredient(self, user_for_test):
        _, access_token = user_for_test
        payload = OrderData.invalid_ingredients_payload
        headers = headers_auth_json(access_token)

        with allure.step("Отправка POST-запроса на создание заказа с авторизацией и неверным хешем ингредиентов"):
            response = requests.post(Urls.MAIN_URL + Handlers.MAKE_ORDER, headers=headers, json=payload)

        with allure.step("Проверка кода ответа"):
            assert response.status_code == OrderResponses.server_error["status_code"]


