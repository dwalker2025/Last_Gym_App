# app.py
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os
from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import datetime, timedelta
from functools import wraps
import requests
import base64
import os
from dotenv import load_dotenv

# Create Flask app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_for_development')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # Session lasts for 7 days

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Specify the login route
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Define models
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    streak_days = db.Column(db.Integer, default=0)
    current_weight = db.Column(db.Float)
    target_weight = db.Column(db.Float)

    # These properties are required by Flask-Login
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def update_streak(self):
        """Update user streak when they log in"""
        today = datetime.utcnow().date()

        if self.last_login is None:
            self.streak_days = 1
        else:
            last_login_date = self.last_login.date()

            # If last login was yesterday, increment streak
            if (today - last_login_date).days == 1:
                self.streak_days += 1
            # If last login was today, keep streak
            elif (today - last_login_date).days == 0:
                pass
            # If last login was more than 1 day ago, reset streak
            else:
                self.streak_days = 1

        self.last_login = datetime.utcnow()

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


@app.route('/register', methods=['GET', 'POST'])
def register():
    # If user is already logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('register.html')

        # Create user
        user, error = User.create_user(username, email, password)

        if error:
            flash(error, 'danger')
            return render_template('register.html')

        # Add user to database
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect to dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        # Get form data
        username_or_email = request.form.get('username_or_email')
        password = request.form.get('password')
        remember = 'remember' in request.form

        # Find user by username or email
        user = User.query.filter((User.username == username_or_email) |
                                 (User.email == username_or_email)).first()

        # Check if user exists and password is correct
        if user and user.check_password(password):
            # Update streak
            user.update_streak()
            db.session.commit()

            # Log the user in
            login_user(user, remember=remember)

            # If there's a 'next' parameter in the URL, redirect there
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Please check your username/email and password.', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('home'))


@app.route('/dashboard')
@login_required
def dashboard():
    # Get current user's stats
    stats = {
        'total_users': User.query.count(),
        'active_users': User.query.filter_by(active=True).count(),
        'recent_joins': User.query.order_by(User.created_at.desc()).limit(5).all(),
        'streak_days': current_user.streak_days,
        'current_weight': current_user.current_weight,
        'target_weight': current_user.target_weight,
        'weight_change': 0  # You'll calculate this based on weight history later
    }
    return render_template('dashboard.html', stats=stats)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


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

load_dotenv()

CLIENT_ID = os.getenv('FATSECRET_CLIENT_ID')
CLIENT_SECRET = os.getenv('FATSECRET_CLIENT_SECRET')
TOKEN_URL = 'https://oauth.fatsecret.com/connect/token'
API_URL = 'https://platform.fatsecret.com/rest/server.api'

def get_access_token():
    # Prepare basic auth
    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials",
        "scope": "basic"
    }

    response = requests.post(TOKEN_URL, headers=headers, data=data)
    return response.json().get("access_token")


@app.route('/search/<query>')
def search_food(query):
    access_token = get_access_token()
    
    params = {
        "method": "foods.search",
        "search_expression": query,
        "format": "json"
    }

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(API_URL, headers=headers, params=params)
    print(response)
    return jsonify(response.json())


if __name__ == '__main__':
    app.run(debug=True)