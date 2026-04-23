from flask import Blueprint, jsonify
from app.controllers.auth_controller import login
from app.decorators.auth_decorator import token_required

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login_route():
    return login()


@auth_bp.route("/protected", methods=["GET"])
@token_required
def protected_route(decoded):
    return jsonify({
        "message": "Access granted",
        "user": decoded
    }), 200


@auth_bp.route("/admin", methods=["GET"])
@token_required
def admin_route(decoded):
    if decoded.get("role") != "admin":
        return jsonify({"message": "Access denied: Admins only"}), 403

    return jsonify({
        "message": "Welcome Admin",
        "user": decoded
    }), 200