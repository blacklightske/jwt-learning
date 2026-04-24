from functools import wraps
from flask import request, jsonify, current_app
from app.utils.jwt_helper import verify_token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs): # Call the original function, pass the decoded user first, and forward any other arguments unchanged.”
         #  /**kwargs means any extra named arguments
        # /*args Means: “any extra positional arguments
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"message": "No token provided"}), 401

        parts = auth_header.split(" ")

        if len(parts) != 2 or parts[0] != "Bearer":
            return jsonify({"message": "Invalid authorization format"}), 401

        token = parts[1]

        try:
            decoded = verify_token(token, current_app.config["SECRET_KEY"])

            if decoded.get("type") != "access":
                return jsonify({
            "message": "Invalid token type: access token required"
        }), 401

            return f(decoded, *args, **kwargs)

        except Exception as e:
            return jsonify({
        "message": "Invalid token",
        "error": str(e)
    }), 401

           

    return decorated

def roles_required(*roles):
    def wrapper(f):
        @wraps(f)
        def decorated(decoded, *args, **kwargs):
            user_role = decoded.get("role")

            if user_role not in roles:
                return jsonify({
                    "message": "Access denied: insufficient permissions"
                }), 403

            return f(decoded, *args, **kwargs)

        return decorated
    return wrapper

#The decorator extracts the token from the request header, verifies it using the
#  secret key, and if valid, passes the decoded user data to the route. If not valid, it blocks the request.
#f is the original route function