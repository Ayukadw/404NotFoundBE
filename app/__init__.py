from flask import Flask
from .extensions import db, migrate, bcrypt, jwt, cors
from .config import Config
from .routes import register_routes
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    from . import models
    bcrypt.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": os.getenv("FRONTEND_URL")}})

    register_routes(app)

    return app
