import jwt
import datetime


def generate_access_token(user, secret_key):
    payload = {
        "sub": str(user["id"]),
        "email": user["email"],
        "role": user["role"],
        "type": "access",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
        "iat": datetime.datetime.utcnow(),
    }

    return jwt.encode(payload, secret_key, algorithm="HS256")


def generate_refresh_token(user, secret_key):
    payload = {
        "sub": str(user["id"]),
        "type": "refresh",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
        "iat": datetime.datetime.utcnow(),
    }

    return jwt.encode(payload, secret_key, algorithm="HS256")


def verify_token(token, secret_key):
    decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
    return decoded