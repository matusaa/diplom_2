import allure
import pytest
import requests
from helpers import Helper
from config import  headers_auth_json
from urls import Urls, Handlers
from data import UpdateUserResponses


@allure.suite('Изменение данных пользователя')
class TestUpdateUserInfo:

    @allure.title("Изменение данных авторизованного пользователя по одному из полей (email, password, name)")
    @pytest.mark.parametrize("field, value_func, result_check",
        [
            (
                "email",
                lambda: Helper.get_user_data()["email"],
                lambda body, payload: body.get('user', {}).get('email') == payload['email']
            ),
            (
                "password",
                lambda: Helper.get_user_data()["password"],
                lambda body, payload: body.get("success") is True
            ),
            (
                "name",
                lambda: Helper.get_user_data()["name"],
                lambda body, payload: body.get('user', {}).get('name') == payload['name']
            ),
        ]
    )
    def test_update_user_field_with_auth(self, user_for_test, field, value_func, result_check):
        payload = {field: value_func()}
        _, access_token = user_for_test
        headers = headers_auth_json(access_token)

        with allure.step(f"Отправка PATCH-запроса на изменение поля '{field}' с авторизацией"):
            response = requests.patch(f"{Urls.MAIN_URL}{Handlers.CHANGE_USER_DATA}", headers=headers, json=payload)

        with allure.step("Проверка кода ответа"):
            assert response.status_code == UpdateUserResponses.success["status_code"]

        with allure.step("Проверка тела ответа"):
            body = response.json()
            assert result_check(body, payload)

    @pytest.mark.parametrize("field",
        ["email", "password", "name"]
    )
    def test_update_user_field_without_auth(self, field):
        payload = {field: Helper.get_user_data()[field]}

        with allure.step(f"Отправка PATCH-запроса на изменение поля '{field}' без авторизации"):
            response = requests.patch(f"{Urls.MAIN_URL}{Handlers.CHANGE_USER_DATA}", json=payload)

        with allure.step("Проверка кода ответа"):
            assert response.status_code == UpdateUserResponses.unauthorized["status_code"]

        with allure.step("Проверка тела ответа"):
            body = response.json()
            assert body.get('success') is UpdateUserResponses.unauthorized["body"]["success"]
            assert body.get('message') == UpdateUserResponses.unauthorized["body"]["message"]