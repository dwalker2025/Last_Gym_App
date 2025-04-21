from flask import Blueprint, jsonify, request
from main.models import User
from app import db
import requests

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def hello_world():
    return 'Hello World!'


# User routes
@main_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = [{"id": user.id, "username": user.username, "email": user.email, "active": user.active} for user in users]
    return jsonify(result)


@main_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "active": user.active,
        "created_at": user.created_at.isoformat()
    })


@main_bp.route('/users', methods=['POST'])
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


@main_bp.route('/users/<int:user_id>', methods=['PUT'])
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


@main_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": f"User {user_id} deleted successfully"})


