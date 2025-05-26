import allure
import requests
from config import Urls, Handlers
from helpers import Helper

@allure.suite('Логин пользователя')
class TestLoginUser:

    @allure.title('Логин под существующим пользователем')
    def test_login_user(self, user_for_test):
        user_data, _ = user_for_test
        login_payload = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        response = requests.post(Urls.MAIN_URL + Handlers.LOGIN,json=login_payload,headers=Handlers.headers_json)

        assert response.status_code == 200
        body = response.json()
        assert body.get("success") == True

    @allure.title('Логин с неверным логином и паролем')
    def test_login_with_invalid_credentials(self):
        login_payload = Helper.data_incorrect
        response = requests.post(Urls.MAIN_URL + Handlers.LOGIN,json=login_payload,headers=Handlers.headers_json)

        assert response.status_code == 401
        body = response.json()
        assert body.get("success") is False
        assert body.get("message") == "email or password are incorrect"