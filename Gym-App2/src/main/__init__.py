# app/__init__.py
from flask import Flask, Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

# Create the extension objects
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)




