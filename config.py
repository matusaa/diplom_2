class Urls:
    MAIN_URL = 'https://stellarburgers.nomoreparties.site'


class Handlers:
    CREATE_USER = '/api/auth/register'
    LOGIN = '/api/auth/login'
    CHANGE_USER_DATA = '/api/auth/user'
    DELETE_USER = '/api/auth/user'
    MAKE_ORDER = '/api/orders'
    GET_ORDERS = '/api/orders'
    GET_INGREDIENTS = '/api/ingredients'

    headers_json = {
        "Content-Type": "application/json"
    }

    headers_auth_json = lambda token: {
        "Content-Type": "application/json",
        "Authorization": token
    }