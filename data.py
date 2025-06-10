class UserData:
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
        "email": "Alexxx19111@mail.ru",
        "password": "654321"
    }

class OrderData:
    valid_ingredients_payload = lambda ingredients: {"ingredients": ingredients}
    empty_ingredients_payload = {"ingredients": []}
    invalid_ingredients_payload = {"ingredients": ["hashinvalid123"]}

class OrderResponses:
    success = {
        "status_code": 200,
        "body": {"success": True}
    }
    missing_ingredients = {
        "status_code": 400,
        "body": {
            "success": False,
            "message": "Ingredient ids must be provided"
        }
    }
    server_error = {
        "status_code": 500
    }

class UserResponses:
    create_success = {
        "status_code": 200,
        "body": {"success": True}
    }

    user_exists = {
        "status_code": 403,
        "body": {"success": False, "message": "User already exists"}
    }

    missing_fields = {
        "status_code": 403,
        "body": {"success": False, "message": "Email, password and name are required fields"}
    }

class GetOrdersResponses:
    authorized_success = {
        "status_code": 200,
        "body": {
            "success": True,
            "orders_type": list
        }
    }

    unauthorized_error = {
        "status_code": 401,
        "body": {
            "success": False,
            "message": "You should be authorised"
        }
    }

class LoginResponses:
    success = {
        "status_code": 200,
        "body": {"success": True}
    }

    invalid_credentials = {
        "status_code": 401,
        "body": {"success": False, "message": "email or password are incorrect"}
    }

class UpdateUserResponses:
    success = {
        "status_code": 200,
        "body": {"success": True}
    }
    unauthorized = {
        "status_code": 401,
        "body": {
            "success": False,
            "message": "You should be authorised"
        }
    }