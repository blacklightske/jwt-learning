from app.utils.jwt_helper import generate_token


fake_user = {
    "id": "1",
    "email": "george@example.com",
    "password": "123456",
    "role": "admin"
}


def login_user(email, password, secret_key):
    if email != fake_user["email"] or password != fake_user["password"]:
        return None

    token = generate_token(fake_user, secret_key)
    return token