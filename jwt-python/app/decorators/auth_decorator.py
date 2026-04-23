from functools import wraps
from flask import request, jsonify, current_app
from app.utils.jwt_helper import verify_token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"message": "No token provided"}), 401

        parts = auth_header.split(" ")

        if len(parts) != 2 or parts[0] != "Bearer":
            return jsonify({"message": "Invalid authorization format"}), 401

        token = parts[1]

        try:
            decoded = verify_token(token, current_app.config["SECRET_KEY"])
            return f(decoded, *args, **kwargs)
        except Exception as e:
            return jsonify({
                "message": "Invalid token",
                "error": str(e)
            }), 401

    return decorated