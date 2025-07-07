from flask import Flask, send_from_directory
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
    cors.init_app(app, resources={r"/api/*": {"origins": os.getenv("FRONTEND_URL")}}, supports_credentials=True, expose_headers=["Authorization"])

    # Test route untuk static files
    @app.route('/test-static/<filename>')
    def test_static(filename):
        upload_folder = os.path.join(os.getcwd(), 'static', 'uploads')
        print(f"Test static - Serving file: {filename} from folder: {upload_folder}")
        print(f"Test static - File exists: {os.path.exists(os.path.join(upload_folder, filename))}")
        return send_from_directory(upload_folder, filename)

    register_routes(app)

    return app
