import allure
import requests
from urls import Urls, Handlers
from config import headers_json
from data import UserData, LoginResponses


@allure.suite('Логин пользователя')
class TestLoginUser:

    @allure.title('Логин под существующим пользователем')
    def test_login_user(self, user_for_test):
        user_data, _ = user_for_test
        login_payload = {
            "email": user_data["email"],
            "password": user_data["password"]
        }

        with allure.step("Отправка POST-запроса на логин с корректными данными"):
            response = requests.post(Urls.MAIN_URL + Handlers.LOGIN, json=login_payload, headers=headers_json)

        with allure.step("Проверка кода ответа"):
            assert response.status_code == LoginResponses.success["status_code"]

        with allure.step("Проверка тела ответа"):
            body = response.json()
            assert body.get("success") is LoginResponses.success["body"]["success"]

    @allure.title('Логин с неверным логином и паролем')
    def test_login_with_invalid_credentials(self):
        login_payload = UserData.data_incorrect

        with allure.step("Отправка POST-запроса на логин с некорректными данными"):
            response = requests.post(Urls.MAIN_URL + Handlers.LOGIN, json=login_payload, headers=headers_json)

        with allure.step("Проверка кода ответа"):
            assert response.status_code == LoginResponses.invalid_credentials["status_code"]

        with allure.step("Проверка тела ответа"):
            body = response.json()
            assert body.get("success") is LoginResponses.invalid_credentials["body"]["success"]
            assert body.get("message") == LoginResponses.invalid_credentials["body"]["message"]