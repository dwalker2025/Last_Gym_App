# app.py
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import datetime

# Create Flask app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_for_development')

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Define models
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def is_valid_email(email):
        """Validate email format - checks for @ symbol and domain"""
        if not email:
            return False

        # Basic pattern: something@something.something
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def is_valid_password(password):
        """
        Validate password strength
        - At least 8 characters long
        """
        if not password or len(password) < 8:
            return False
        return True

    @classmethod
    def create_user(cls, username, email, password):
        """
        Create a new user with validation
        Returns (user, error_message)
        """
        # Validate email
        if not cls.is_valid_email(email):
            return None, "Invalid email format"

        # Check if email already exists
        if cls.query.filter_by(email=email).first():
            return None, "Email already registered"

        # Check if username already exists
        if cls.query.filter_by(username=username).first():
            return None, "Username already taken"

        # Validate password
        if not cls.is_valid_password(password):
            return None, "Password must be at least 8 characters long"

        # Create new user
        user = cls(username=username, email=email, password=password)
        return user, None


# Web UI Routes
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/dashboard')
def dashboard():
    # For now, just display a placeholder dashboard
    # Later, you can add authentication and personalized content
    stats = {
        'total_users': User.query.count(),
        'active_users': User.query.filter_by(active=True).count(),
        'recent_joins': User.query.order_by(User.created_at.desc()).limit(5).all()
    }
    return render_template('dashboard.html', stats=stats)


@app.route('/about')
def about():
    return render_template('about.html')


# API Routes
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = [{"id": user.id, "username": user.username, "email": user.email, "active": user.active} for user in users]
    return jsonify(result)


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "active": user.active,
        "created_at": user.created_at.isoformat()
    })


@app.route('/api/users', methods=['POST'])
def create_user():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    user, error = User.create_user(username, email, password)

    if error:
        return jsonify({"error": error}), 400

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "message": "User created successfully"
    }), 201


@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)

    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    if 'username' in data:
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user and existing_user.id != user.id:
            return jsonify({"error": "Username already taken"}), 400
        user.username = data['username']

    if 'email' in data:
        if not User.is_valid_email(data['email']):
            return jsonify({"error": "Invalid email format"}), 400

        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != user.id:
            return jsonify({"error": "Email already registered"}), 400
        user.email = data['email']

    if 'password' in data:
        if not User.is_valid_password(data['password']):
            return jsonify({"error": "Password must be at least 8 characters long"}), 400
        user.set_password(data['password'])

    if 'active' in data and isinstance(data['active'], bool):
        user.active = data['active']

    db.session.commit()

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "active": user.active,
        "message": "User updated successfully"
    })


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": f"User {user_id} deleted successfully"})


if __name__ == '__main__':
    app.run(debug=True)