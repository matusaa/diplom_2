headers_json = {
    "Content-Type": "application/json"
}

headers_auth_json = lambda token: {
    "Content-Type": "application/json",
    "Authorization": token
}