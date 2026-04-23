from flask import request, jsonify, current_app
from app.services.auth_service import login_user


def login():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Request body must be JSON"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    token = login_user(email, password, current_app.config["SECRET_KEY"])

    if not token:
        return jsonify({"message": "Invalid credentials"}), 401

    return jsonify({
        "message": "Login successful",
        "token": token
    }), 200