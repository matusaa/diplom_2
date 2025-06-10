import pytest
import allure
import requests
from urls import Urls, Handlers
from config import headers_json
from helpers import Helper
from data import UserData, UserResponses


@allure.suite('Создание пользователя')
class TestCreateUser:

    @allure.title('Создание уникального пользователя')
    def test_create_unique_user(self):
        user_data = Helper.get_user_data()
        with allure.step("Отправка POST-запроса на создание уникального пользователя"):
            response = requests.post(Urls.MAIN_URL + Handlers.CREATE_USER, json=user_data, headers=headers_json)

        with allure.step("Проверка кода ответа"):
            assert response.status_code == UserResponses.create_success["status_code"]

        with allure.step("Проверка тела ответа"):
            body = response.json()
            assert body.get("success") is UserResponses.create_success["body"]["success"]

    @allure.title('Создание пользователя, который уже зарегистрирован')
    def test_create_user_already_registered(self, user_for_test):
        user_data, _ = user_for_test
        with allure.step("Отправка POST-запроса на создание уже зарегистрированного пользователя"):
            response = requests.post(Urls.MAIN_URL + Handlers.CREATE_USER, json=user_data, headers=headers_json)

        with allure.step("Проверка кода ответа"):
            assert response.status_code == UserResponses.user_exists["status_code"]

        with allure.step("Проверка тела ответа"):
            body = response.json()
            assert body.get("success") is UserResponses.user_exists["body"]["success"]
            assert body.get("message") == UserResponses.user_exists["body"]["message"]

    @allure.title('Создание пользователя с одним незаполненным обязательным полем')
    @pytest.mark.parametrize("user_data, missing_field",
        [
            (UserData.data_without_email, "email"),
            (UserData.data_without_password, "password"),
            (UserData.data_without_name, "name"),
        ]
    )
    def test_create_user_without_required_field(self, user_data, missing_field):
        with allure.step(f"Попытка создать пользователя без поля: {missing_field}"):
            response = requests.post(Urls.MAIN_URL + Handlers.CREATE_USER, json=user_data, headers=headers_json)

        with allure.step("Проверка кода ответа"):
            assert response.status_code == UserResponses.missing_fields["status_code"]

        with allure.step("Проверка тела ответа"):
            body = response.json()
            assert body.get("success") is UserResponses.missing_fields["body"]["success"]
            assert body.get("message") == UserResponses.missing_fields["body"]["message"]