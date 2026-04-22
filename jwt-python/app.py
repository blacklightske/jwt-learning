from flask import Flask, jsonify, request
import jwt
import datetime

app = Flask(__name__)

SECRET_KEY = "my_super_secret_key"

fake_user = {
    "id": "1",
    "email": "george@example.com",
    "password": "123456",
    "role": "admin",
}


@app.route("/")
def home():
    return jsonify({"message": "Flask JWT app running"})


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Request body must be JSON"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    if email != fake_user["email"] or password != fake_user["password"]:
        return jsonify({"message": "Invalid credentials"}), 401

    payload = {
        "sub": fake_user["id"],
        "id": fake_user["id"],
        "email": fake_user["email"],
        "role": fake_user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        "iat": datetime.datetime.utcnow(),
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return jsonify({
        "message": "Login successful",
        "token": token
    })


@app.route("/protected")
def protected():
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return jsonify({"message": "No token provided"}), 401

    try:
        parts = auth_header.split(" ")

        if len(parts) != 2 or parts[0] != "Bearer":
            return jsonify({"message": "Invalid authorization format"}), 401

        token = parts[1]
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        return jsonify({
            "message": "Access granted",
            "user": decoded
        })

    except Exception as e:
        return jsonify({
            "message": "Invalid token",
            "error": str(e)
        }), 401

@app.route("/admin")
def admin():
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return jsonify({"message": "No token provided"}), 401

    try:
        parts = auth_header.split(" ")

        if len(parts) != 2 or parts[0] != "Bearer":
            return jsonify({"message": "Invalid authorization format"}), 401

        token = parts[1]
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        # 🔥 ROLE CHECK
        if decoded.get("role") != "admin":
            return jsonify({"message": "Access denied: Admins only"}), 403

        return jsonify({
            "message": "Welcome Admin",
            "user": decoded
        })

    except Exception as e:
        return jsonify({
            "message": "Invalid token",
            "error": str(e)
        }), 401

if __name__ == "__main__":
    app.run(debug=True)