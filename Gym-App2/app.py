# app.py
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os
from datetime import timedelta
import json
from dotenv import load_dotenv
import base64
import requests

# Import models
from models import db, User, Restriction, Response

# Create Flask app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_for_development')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # Session lasts for 7 days

# Initialize extensions
db.init_app(app)  # Initialize db with app
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Specify the login route
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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
        user, error = User.create_user(username=username, email=email, password=password)

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
        'current_weight': current_user.weight,
        'target_weight': current_user.target_weight,
        'weight_change': 0  # You'll calculate this based on weight history later
    }
    return render_template('dashboard.html', stats=stats)


@app.route('/foodDisplay',methods=['GET', 'POST'])
@login_required
def food_display():
    
    if request.method == 'POST':
        # Get form data
        search = request.form.get('foodSearch')
        current_response = Response.query.filter((Response.search == search)).first()
        data = current_response
        if (data == None):
            data = internal_search_food(query=search)
            try:
                x = data["foods"]
                newResponse = Response(search = search, last_searched =Response.get_time(), returned_data = data)
                db.session.add(newResponse)
                db.session.commit()
            except(KeyError):
                print("Error: api did not return a valid response")
                print("Response was: ")
                print(data)
                return render_template('foodDisplay.html', foodList={})
            
        else:
            data = data.get_data()
        #print(type(foodList))
        #print(foodList['foods']['food'])
        return render_template('foodDisplay.html', foodList=data)
    else:
        return render_template('foodDisplay.html', foodList={})


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        # Update user profile data
        current_user.username = request.form.get('username', current_user.username)

        # Update physical attributes
        if request.form.get('height'):
            current_user.height = int(request.form.get('height'))
        if request.form.get('weight'):
            current_user.weight = int(request.form.get('weight'))
        if request.form.get('target_weight'):
            current_user.target_weight = float(request.form.get('target_weight'))

        # Update goals if provided
        if request.form.get('goals'):
            goals = request.form.get('goals').split(',')
            current_user.goals = json.dumps([goal.strip() for goal in goals])

        # Save changes
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile'))

    return render_template('edit_profile.html', user=current_user)


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

    # Optional parameters
    height = data.get('height')
    weight = data.get('weight')
    target_weight = data.get('target_weight')
    availability = data.get('availability')
    goals = data.get('goals')

    user, error = User.create_user(
        username=username,
        email=email,
        password=password,
        height=height,
        weight=weight,
        availability=availability,
        goals=goals,
        target_weight=target_weight
    )

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

    if 'height' in data:
        user.height = data['height']

    if 'weight' in data:
        user.weight = data['weight']

    if 'target_weight' in data:
        user.target_weight = data['target_weight']

    if 'goals' in data:
        user.goals = json.dumps(data['goals'])

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
    #print(response)
    return jsonify(response.json())

def internal_search_food(query):
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
    #print(response)
    return response.json()

def internal_full_API_Method(query):
    current_response = Response.query.filter((Response.search == query)).first()
    data = current_response
    if (data == None):
        data = internal_search_food(query=query)
        try:
            x = data["foods"]
            newResponse = Response(search = query, last_searched =Response.get_time(), returned_data = data)
            #db.session.add(newResponse)
            #db.session.commit()
        except(KeyError):
            print("Error: api did not return a valid response")
            print("Response was: ")
            print(data)
            return {}
    else:
        data = data.get_data()
        return data


if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
    app.run(debug=True)