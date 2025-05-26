import allure
import requests
from config import Urls, Handlers
from helpers import Helper

@allure.suite("Создание заказа")
class TestCreateOrder:
    @allure.title("Создание заказа с авторизацией и валидными ингредиентами")
    def test_create_order_with_valid_ingredients(self, user_for_test):
        _, access_token = user_for_test
        ingredients = Helper.get_ingredients_ids()[:2]
        payload = {"ingredients": ingredients}
        headers = Handlers.headers_auth_json(access_token)
        response = requests.post(Urls.MAIN_URL + Handlers.MAKE_ORDER, headers=headers, json=payload)
        assert response.status_code == 200
        body = response.json()
        assert body.get("success") is True

    @allure.title("Создание заказа без авторизации и валидными ингредиентами")
    def test_create_order_without_auth(self):
        ingredients = Helper.get_ingredients_ids()[:2]
        payload = {"ingredients": ingredients}
        response = requests.post(Urls.MAIN_URL + Handlers.MAKE_ORDER, json=payload)
        assert response.status_code == 200
        body = response.json()
        assert body.get("success") is True

    @allure.title("Создание заказа с авторизацией и без ингредиентов")
    def test_create_order_with_auth_without_ingredients(self, user_for_test):
        _, access_token = user_for_test
        payload = {"ingredients": []}
        headers = Handlers.headers_auth_json(access_token)
        response = requests.post(Urls.MAIN_URL + Handlers.MAKE_ORDER, headers=headers, json=payload)
        assert response.status_code == 400
        body = response.json()
        assert body.get("success") is False
        assert body.get("message") == "Ingredient ids must be provided"

    @allure.title("Создание заказа без авторизации и без ингредиентов")
    def test_create_order_without_auth_without_ingredients(self):
        payload = {"ingredients": []}
        response = requests.post(Urls.MAIN_URL + Handlers.MAKE_ORDER, json=payload)
        assert response.status_code == 400
        body = response.json()
        assert body.get("success") is False
        assert body.get("message") == "Ingredient ids must be provided"

    @allure.title("Создание заказа c неверным хешем ингредиентов")
    def test_create_order_with_auth_invalid_ingredient(self, user_for_test):
        _, access_token = user_for_test
        payload = {"ingredients": ["hashinvalid123"]}
        headers = Handlers.headers_auth_json(access_token)
        response = requests.post(Urls.MAIN_URL + Handlers.MAKE_ORDER, headers=headers, json=payload)
        assert response.status_code == 500


