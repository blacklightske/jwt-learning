from flask import Flask
from app.config import Config


def create_app():
    app = Flask(__name__)
    # load config
    app.config.from_object(Config)

    #register routes
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app