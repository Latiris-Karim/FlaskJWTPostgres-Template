from flask import Flask
from dotenv import load_dotenv
import os
from flask_jwt_extended import (
    JWTManager
)

from datetime import timedelta
def create_app():
    app = Flask(__name__)
    load_dotenv()
    secretkey = os.getenv("JWT_SECRET_KEY")
    app.config['JWT_SECRET_KEY'] = secretkey  # Change this to a secure secret key
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    JWTManager(app)

    # Import blueprints from the routes module
    from .routes.controller_userauth import users
    # Register the blueprint
    app.register_blueprint(users, url_prefix='/users')
    return app
