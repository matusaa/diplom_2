import pytest
from helpers import Helper

@pytest.fixture
def user_for_test():
    user_data = Helper.get_user_data()
    response = Helper.create_user(user_data)
    assert response.status_code == 200
    access_token = response.json().get("accessToken")
    yield user_data, access_token

    if access_token:
        Helper.delete_user(access_token)