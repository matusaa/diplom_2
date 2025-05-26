import pytest
import allure
import requests
from config import Urls, Handlers
from helpers import Helper

@allure.suite('Создание пользователя')
class TestCreateUser:

    @allure.title('Создание уникального пользователя')
    def test_create_unique_user(self):
        user_data = Helper.get_user_data()
        response = requests.post(Urls.MAIN_URL + Handlers.CREATE_USER, json=user_data, headers=Handlers.headers_json)

        assert response.status_code == 200
        body = response.json()
        assert body.get("success") is True

    @allure.title('Создание пользователя, который уже зарегистрирован')
    def test_create_user_already_registered(self, user_for_test):
        user_data, _ = user_for_test
        response = requests.post(Urls.MAIN_URL + Handlers.CREATE_USER, json=user_data, headers=Handlers.headers_json)

        assert response.status_code == 403
        body = response.json()
        assert body.get("success") is False
        assert body.get("message") == "User already exists"

    @allure.title('Создание пользователя с одним незаполненным обязательным полем')
    @pytest.mark.parametrize("user_data, missing_field",
        [
            (Helper.data_without_email, "email"),
            (Helper.data_without_password, "password"),
            (Helper.data_without_name, "name"),
        ]
    )
    def test_create_user_without_required_field(self, user_data, missing_field):
        with allure.step(f"Попытка создать пользователя без поля: {missing_field}"):
            response = requests.post(Urls.MAIN_URL + Handlers.CREATE_USER, json=user_data, headers=Handlers.headers_json)

        assert response.status_code == 403
        body = response.json()
        assert body.get("success") is False
        assert body.get("message") == "Email, password and name are required fields"