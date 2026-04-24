from app.db import get_db_connection
from app.utils.jwt_helper import generate_access_token, generate_refresh_token
from app.utils.password_helper import check_password
from app.utils.password_helper import hash_password


def find_user_by_email(email):
    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE email = %s"
            cursor.execute(sql, (email,))
            user = cursor.fetchone()
            return user
    finally:
        connection.close()


def login_user(email, password, secret_key):
    user = find_user_by_email(email)

    if not user:
        return None

    if not check_password(password, user["password"]):
        return None

    access_token = generate_access_token(user, secret_key)
    refresh_token = generate_refresh_token(user, secret_key)

    return {
    "access_token": access_token,
    "refresh_token": refresh_token
}
def register_user(email, password, role="user"):
    existing_user = find_user_by_email(email)

    if existing_user:
        return None

    hashed_password = hash_password(password)

    connection = get_db_connection()

    try:
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO users (email, password, role)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (email, hashed_password, role))
            connection.commit()

            return {
                "email": email,
                "role": role
            }
    finally:
        connection.close()