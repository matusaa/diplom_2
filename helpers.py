from faker import Faker
import requests
from config import Urls, Handlers

fake = Faker()

class Helper:

    @staticmethod
    def generate_unique_email():
        return fake.unique.email(domain='mail.ru')

    @staticmethod
    def get_user_data():
        return {
            "email": Helper.generate_unique_email(),
            "password": fake.password(length=8),
            "name": fake.first_name()
        }

    @staticmethod
    def create_user(user_data):
        response = requests.post(
            Urls.MAIN_URL + Handlers.CREATE_USER,
            json=user_data,
            headers=Handlers.headers_json
        )
        return response

    @staticmethod
    def delete_user(access_token):
        response = requests.delete(
            Urls.MAIN_URL + Handlers.DELETE_USER,
            headers=Handlers.headers_auth_json(access_token)
        )
        return response

    @staticmethod
    def get_ingredients_ids():
        response = requests.get(Urls.MAIN_URL + Handlers.GET_INGREDIENTS)
        response.raise_for_status()
        data = response.json()
        return [item["_id"] for item in data["data"]]

    data_without_email = {
        "password": "123456",
        "name": "Alex"
    }

    data_without_password = {
        "email": "Alex19111@mail.ru",
        "name": "Alex"
    }

    data_without_name = {
        "email": "Alex19111@mail.ru",
        "password": "123456"
    }

    data_incorrect = {
        "email": 'Alexxx19111@mail.ru',
        "password": "654321"
    }