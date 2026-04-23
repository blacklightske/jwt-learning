import jwt
import datetime


def generate_token(user, secret_key):
    payload = {
        "sub": user["id"],
        "email": user["email"],
        "role": user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        "iat": datetime.datetime.utcnow(),
    }

    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


def verify_token(token, secret_key):
    decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
    return decoded