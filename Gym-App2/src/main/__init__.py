# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Create the extension objects
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    # Create the Flask app
    app = Flask(__name__)

    # Configure the Flask app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_for_development')

    # Initialize extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app


