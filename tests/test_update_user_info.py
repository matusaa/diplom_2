import pytest
import allure
import requests
from config import Urls, Handlers
from helpers import Helper

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
        user_data, access_token = user_for_test
        payload = {field: value_func()}
        headers = Handlers.headers_auth_json(access_token)
        response = requests.patch(f"{Urls.MAIN_URL}{Handlers.CHANGE_USER_DATA}", headers=headers, json=payload)
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        body = response.json()
        assert result_check(body, payload)

    @allure.title("Изменения данных пользователя без авторизации")
    @pytest.mark.parametrize("field, value_func",
        [
            ("email", lambda: Helper.get_user_data()["email"]),
            ("password", lambda: Helper.get_user_data()["password"]),
            ("name", lambda: Helper.get_user_data()["name"]),
        ]
    )
    def test_update_user_field_without_auth(self, field, value_func):
        payload = {field: value_func()}
        response = requests.patch(f"{Urls.MAIN_URL}{Handlers.CHANGE_USER_DATA}",json=payload)
        assert response.status_code == 401
        body = response.json()
        assert body.get('success') is False
        assert body.get('message') == "You should be authorised"