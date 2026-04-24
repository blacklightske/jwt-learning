from flask import request, jsonify, current_app
from app.services.auth_service import login_user
from app.services.auth_service import login_user, register_user  


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

def register():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Request body must be JSON"}), 400

    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "user")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    new_user = register_user(email, password, role)

    if not new_user:
        return jsonify({"message": "User already exists"}), 409

    return jsonify({
        "message": "User registered successfully",
        "user": new_user
    }), 201