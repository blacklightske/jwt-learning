from flask import Blueprint, jsonify
from app.decorators.auth_decorator import token_required, roles_required
from app.controllers.auth_controller import login, register

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login_route():
    return login()

@auth_bp.route("/register", methods=["POST"])
def register_route():
    return register()


@auth_bp.route("/protected", methods=["GET"])
@token_required
def protected_route(decoded):
    return jsonify({
        "message": "Access granted",
        "user": decoded
    }), 200

@auth_bp.route("/admin", methods=["GET"])
@token_required
@roles_required("admin")
def admin_route(decoded):
    return jsonify({
        "message": "Welcome Admin",
        "user": decoded
    }), 200