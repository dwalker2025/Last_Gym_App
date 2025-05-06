# app.py
from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os
from datetime import timedelta
from datetime import date
from datetime import datetime
import json
from dotenv import load_dotenv
import base64
import requests

# Import models
from models import db, User, Restriction, Meal, Exercise, WorkoutTemplate, Workout, UserMealPlan

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

@app.context_processor
def inject_now():
    from datetime import datetime
    return {'now': datetime.now()}

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
        'streak_days': current_user.streak_days,
        'current_weight': current_user.weight,
        'target_weight': current_user.target_weight,
        'weight_change': 0  # You'll calculate this based on weight history later

    }

    # Get meal recommendations
    meal_plan = Meal.get_personalized_meals(current_user)

    # Get workout recommendations
    workout_plan = WorkoutTemplate.get_personalized_workouts(current_user) if hasattr(WorkoutTemplate,
                                                                                      'get_personalized_workouts') else []

    # Get user's upcoming workouts and meals
    calendar_data = current_user.get_calendar_data() if hasattr(current_user, 'get_calendar_data') else {}

    return render_template('dashboard.html', stats=stats, meal_plan=meal_plan, workout_plan=workout_plan,
                           calendar_data=calendar_data)


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

        # Update dietary preferences and fitness goals
        current_user.dietary_preference = request.form.get('dietary_preference')
        current_user.fitness_goal = request.form.get('fitness_goal')

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


# New Routes for Meals and Workouts
@app.route('/meals', methods=['GET', 'POST'])
@login_required
def meals():
    if request.method == 'POST':
        # Update user's dietary preferences
        current_user.dietary_preference = request.form.get('dietary_preference')
        current_user.fitness_goal = request.form.get('fitness_goal')

        # Handle preferred proteins
        preferred_proteins = request.form.getlist('preferred_proteins')
        current_user.preferred_proteins = json.dumps(preferred_proteins) if preferred_proteins else json.dumps([])

        # Handle disliked foods
        disliked_foods = request.form.get('disliked_foods', '').split(',')
        current_user.disliked_foods = json.dumps([food.strip() for food in disliked_foods if food.strip()])

        # Handle allergies
        allergies = request.form.get('allergies', '').split(',')
        current_user.allergies = json.dumps([allergy.strip() for allergy in allergies if allergy.strip()])

        # Create or update restrictions
        if not current_user.restrictions:
            restrictions = Restriction(user_id=current_user.id)
            db.session.add(restrictions)
        else:
            restrictions = current_user.restrictions

        # Update dietary restrictions
        dietary_restrictions = request.form.get('dietary_restrictions', '').split(',')
        restrictions.dietary_restrictions = json.dumps(
            [restriction.strip() for restriction in dietary_restrictions if restriction.strip()])

        db.session.commit()
        flash('Dietary preferences updated successfully!', 'success')

        # Generate a meal plan for the user
        return redirect(url_for('meal_plan'))

    # For GET request, show the form with current preferences
    dietary_types = ['omnivore', 'vegetarian', 'vegan', 'pescatarian', 'keto', 'paleo']
    fitness_goals = ['bulking', 'cutting', 'maintenance']
    protein_sources = ['chicken', 'beef', 'pork', 'fish', 'eggs', 'tofu', 'tempeh', 'legumes', 'dairy']

    current_proteins = current_user.get_preferred_proteins() if current_user.preferred_proteins else []
    current_dislikes = current_user.get_disliked_foods() if current_user.disliked_foods else []
    current_allergies = current_user.get_allergies() if current_user.allergies else []
    current_restrictions = current_user.restrictions.get_dietary_restrictions() if current_user.restrictions else []

    return render_template(
        'meals.html',
        dietary_types=dietary_types,
        fitness_goals=fitness_goals,
        protein_sources=protein_sources,
        current_proteins=current_proteins,
        current_dislikes=current_dislikes,
        current_allergies=current_allergies,
        current_restrictions=current_restrictions
    )


@app.route('/meal-plan')
@login_required
def meal_plan():
    # Generate personalized meal plan
    meal_plan = Meal.get_personalized_meals(current_user)

    # Create a new meal plan entry for today if needed
    # This is optional and would allow tracking which meals the user selects

    return render_template('meal_plan.html', meal_plan=meal_plan)


@app.route('/save-meal-plan', methods=['POST'])
@login_required
def save_meal_plan():
    # Save the selected meal plan
    breakfast_id = request.form.get('breakfast_id')
    lunch_id = request.form.get('lunch_id')
    dinner_id = request.form.get('dinner_id')
    snacks = request.form.getlist('snack_id')

    # Create a new meal plan for the user
    meal_plan = UserMealPlan(
        user_id=current_user.id,
        breakfast_id=breakfast_id,
        lunch_id=lunch_id,
        dinner_id=dinner_id,
        snacks=json.dumps(snacks) if snacks else json.dumps([])
    )

    db.session.add(meal_plan)
    db.session.commit()

    flash('Your meal plan has been saved!', 'success')
    return redirect(url_for('dashboard'))


@app.route('/workouts', methods=['GET', 'POST'])
@login_required
def workouts():
    if request.method == 'POST':
        # Update user's workout preferences
        current_user.fitness_goal = request.form.get('fitness_goal')
        current_user.workout_experience = request.form.get('workout_experience')
        current_user.workout_days_per_week = int(request.form.get('workout_days_per_week', 3))
        current_user.workout_duration = int(request.form.get('workout_duration', 45))

        # Create or update restrictions
        if not current_user.restrictions:
            restrictions = Restriction(user_id=current_user.id)
            db.session.add(restrictions)
        else:
            restrictions = current_user.restrictions

        # Update physical restrictions
        injury_areas = request.form.getlist('injury_areas')
        restrictions.injury_areas = json.dumps(injury_areas) if injury_areas else json.dumps([])

        limited_movements = request.form.get('limited_movements', '').split(',')
        restrictions.limited_movements = json.dumps(
            [movement.strip() for movement in limited_movements if movement.strip()])

        db.session.commit()
        flash('Workout preferences updated successfully!', 'success')
        return redirect(url_for('workout_plan'))

    # For GET request, show the form with current preferences
    fitness_goals = ['bulking', 'cutting', 'maintenance', 'strength', 'endurance', 'flexibility']
    experience_levels = ['beginner', 'intermediate', 'advanced']
    body_parts = ['shoulders', 'arms', 'chest', 'back', 'abs', 'legs', 'knees', 'ankles', 'wrists', 'neck']

    current_injuries = []
    current_movements = []

    if current_user.restrictions:
        current_injuries = current_user.restrictions.get_injury_areas()
        current_movements = current_user.restrictions.get_limited_movements()

    return render_template(
        'workouts.html',
        fitness_goals=fitness_goals,
        experience_levels=experience_levels,
        body_parts=body_parts,
        current_injuries=current_injuries,
        current_movements=current_movements
    )


@app.route('/workout-plan')
@login_required
def workout_plan():
    # Generate personalized workout plan
    workout_templates = WorkoutTemplate.get_personalized_workouts(current_user)

    # Get exercise details for each workout
    workout_plans = []

    for template in workout_templates:
        exercises = []
        for exercise_data in template.get_exercises():
            exercise_id = exercise_data.get('exercise_id')
            if exercise_id:
                exercise = Exercise.query.get(exercise_id)
                if exercise:
                    exercises.append({
                        'exercise': exercise,
                        'sets': exercise_data.get('sets', 3),
                        'reps': exercise_data.get('reps', 10),
                        'rest': exercise_data.get('rest', 60)  # Rest in seconds
                    })

        workout_plans.append({
            'template': template,
            'exercises': exercises
        })

    return render_template('workout_plan.html', workout_plans=workout_plans)


@app.route('/save-workout', methods=['POST'])
@login_required
def save_workout():
    # Save a workout plan for the user
    template_id = request.form.get('template_id')
    template = WorkoutTemplate.query.get(template_id)

    if not template:
        flash('Invalid workout template', 'danger')
        return redirect(url_for('workout_plan'))

    # Create a new workout for the user
    workout = Workout(
        user_id=current_user.id,
        workout_template_id=template_id,
        workout_name=template.name,
        duration=template.duration,
        completed=False,
        exercises_completed=template.exercises  # Initially copy the template's exercises
    )

    db.session.add(workout)
    db.session.commit()

    flash('Workout has been added to your plan!', 'success')
    return redirect(url_for('dashboard'))


@app.route('/search/<query>')
def search_food(query):
    load_dotenv()
    CLIENT_ID = os.getenv('FATSECRET_CLIENT_ID')
    CLIENT_SECRET = os.getenv('FATSECRET_CLIENT_SECRET')
    TOKEN_URL = 'https://oauth.fatsecret.com/connect/token'
    API_URL = 'https://platform.fatsecret.com/rest/server.api'

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
    access_token = response.json().get("access_token")

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


# Add to app.py
@app.cli.command("seed-meals")
def seed_meals():
    """Seed the database with meal options"""
    # Clear existing meals
    Meal.query.delete()

    # Sample meals
    meals = [
        # Bulking - Omnivore
        Meal(name="Protein-Packed Oatmeal", description="Oatmeal with protein powder, banana, and peanut butter",
             calories=650, protein=40, carbs=70, fats=20, meal_type="breakfast", dietary_type="omnivore",
             fitness_goal="bulking"),
        Meal(name="Steak and Eggs", description="Ribeye steak with 3 scrambled eggs and toast",
             calories=800, protein=60, carbs=30, fats=45, meal_type="breakfast", dietary_type="omnivore",
             fitness_goal="bulking"),
        Meal(name="Chicken Rice Bowl", description="Grilled chicken, brown rice, avocado, and vegetables",
             calories=750, protein=45, carbs=80, fats=20, meal_type="lunch", dietary_type="omnivore",
             fitness_goal="bulking"),
        Meal(name="Beef Burrito", description="Ground beef, beans, rice, cheese in a large tortilla",
             calories=900, protein=50, carbs=90, fats=35, meal_type="lunch", dietary_type="omnivore",
             fitness_goal="bulking"),
        Meal(name="Salmon with Quinoa", description="Baked salmon with quinoa and roasted vegetables",
             calories=700, protein=40, carbs=60, fats=30, meal_type="dinner", dietary_type="omnivore",
             fitness_goal="bulking"),
        Meal(name="Protein Shake", description="Whey protein with milk, banana, and peanut butter",
             calories=400, protein=30, carbs=40, fats=10, meal_type="snack", dietary_type="omnivore",
             fitness_goal="bulking"),

        # Cutting - Omnivore
        Meal(name="Egg White Omelette", description="Egg whites with spinach, tomato and feta cheese",
             calories=300, protein=25, carbs=10, fats=15, meal_type="breakfast", dietary_type="omnivore",
             fitness_goal="cutting"),
        Meal(name="Greek Yogurt with Berries",
             description="Low-fat Greek yogurt with mixed berries and a dash of honey",
             calories=250, protein=20, carbs=25, fats=5, meal_type="breakfast", dietary_type="omnivore",
             fitness_goal="cutting"),
        Meal(name="Grilled Chicken Salad",
             description="Grilled chicken breast on a bed of mixed greens with light dressing",
             calories=350, protein=35, carbs=15, fats=15, meal_type="lunch", dietary_type="omnivore",
             fitness_goal="cutting"),
        Meal(name="Tuna Wrap", description="Tuna with light mayo, lettuce and tomato in a whole grain wrap",
             calories=400, protein=30, carbs=40, fats=10, meal_type="lunch", dietary_type="omnivore",
             fitness_goal="cutting"),
        Meal(name="White Fish with Vegetables", description="Baked cod with steamed broccoli and cauliflower",
             calories=300, protein=30, carbs=15, fats=10, meal_type="dinner", dietary_type="omnivore",
             fitness_goal="cutting"),
        Meal(name="Protein Shake", description="Whey protein with water and ice",
             calories=120, protein=25, carbs=2, fats=1, meal_type="snack", dietary_type="omnivore",
             fitness_goal="cutting"),

        # Bulking - Vegan
        Meal(name="Tofu Scramble", description="Tofu scrambled with nutritional yeast, vegetables and spices",
             calories=450, protein=25, carbs=30, fats=25, meal_type="breakfast", dietary_type="vegan",
             fitness_goal="bulking"),
        Meal(name="Protein Pancakes", description="Vegan pancakes made with plant protein, bananas and almond milk",
             calories=600, protein=30, carbs=80, fats=15, meal_type="breakfast", dietary_type="vegan",
             fitness_goal="bulking"),
        Meal(name="Tempeh Buddha Bowl", description="Marinated tempeh with quinoa, avocado, and roasted vegetables",
             calories=700, protein=35, carbs=75, fats=30, meal_type="lunch", dietary_type="vegan",
             fitness_goal="bulking"),
        Meal(name="Lentil Pasta", description="High-protein lentil pasta with tomato sauce and nutritional yeast",
             calories=650, protein=40, carbs=85, fats=15, meal_type="dinner", dietary_type="vegan",
             fitness_goal="bulking"),
        Meal(name="Chickpea Curry", description="Spicy chickpea curry with coconut milk and brown rice",
             calories=750, protein=30, carbs=90, fats=25, meal_type="dinner", dietary_type="vegan",
             fitness_goal="bulking"),
        Meal(name="Trail Mix", description="Mix of nuts, seeds, and dried fruits",
             calories=350, protein=10, carbs=25, fats=25, meal_type="snack", dietary_type="vegan",
             fitness_goal="bulking"),

        # Cutting - Vegan
        Meal(name="Green Smoothie Bowl",
             description="Spinach, kale, plant protein, and berries blended with almond milk",
             calories=300, protein=20, carbs=40, fats=5, meal_type="breakfast", dietary_type="vegan",
             fitness_goal="cutting"),
        Meal(name="Overnight Chia Pudding", description="Chia seeds soaked in almond milk with cinnamon and berries",
             calories=250, protein=15, carbs=30, fats=10, meal_type="breakfast", dietary_type="vegan",
             fitness_goal="cutting"),
        Meal(name="Zucchini Noodles with Tofu", description="Spiralized zucchini with grilled tofu and tomato sauce",
             calories=300, protein=20, carbs=30, fats=10, meal_type="lunch", dietary_type="vegan",
             fitness_goal="cutting"),
        Meal(name="Cauliflower Rice Stir-fry",
             description="Cauliflower rice with tofu, broccoli, and low-sodium soy sauce",
             calories=350, protein=25, carbs=25, fats=15, meal_type="dinner", dietary_type="vegan",
             fitness_goal="cutting"),
        Meal(name="Edamame", description="Steamed edamame pods with sea salt",
             calories=150, protein=15, carbs=10, fats=5, meal_type="snack", dietary_type="vegan",
             fitness_goal="cutting")
    ]

    # Add to database
    for meal in meals:
        db.session.add(meal)

    db.session.commit()
    print("Database seeded with meal options!")


@app.cli.command("seed-exercises")
def seed_exercises():
    """Seed the database with exercise options"""
    # Clear existing exercises
    Exercise.query.delete()

    # Sample exercises
    exercises = [
        # Chest exercises
        Exercise(name="Push-up", description="Standard push-up exercise targeting chest, shoulders, and triceps",
                 muscle_group="chest", difficulty="beginner", equipment_needed=json.dumps(["none"]),
                 contraindications=json.dumps(["wrist injury", "shoulder injury"])),
        Exercise(name="Bench Press", description="Barbell bench press for chest development",
                 muscle_group="chest", difficulty="intermediate", equipment_needed=json.dumps(["barbell", "bench"]),
                 contraindications=json.dumps(["shoulder injury"])),
        Exercise(name="Dumbbell Fly", description="Dumbbell fly movement for chest isolation",
                 muscle_group="chest", difficulty="intermediate", equipment_needed=json.dumps(["dumbbells", "bench"]),
                 contraindications=json.dumps(["shoulder injury"])),

        # Back exercises
        Exercise(name="Pull-up", description="Body weight pull-up for back and biceps",
                 muscle_group="back", difficulty="intermediate", equipment_needed=json.dumps(["pull-up bar"]),
                 contraindications=json.dumps(["shoulder injury", "elbow injury"])),
        Exercise(name="Bent-over Row", description="Barbell bent-over row for back development",
                 muscle_group="back", difficulty="intermediate", equipment_needed=json.dumps(["barbell"]),
                 contraindications=json.dumps(["lower back injury"])),
        Exercise(name="Lat Pulldown", description="Cable lat pulldown for back width",
                 muscle_group="back", difficulty="beginner", equipment_needed=json.dumps(["cable machine"]),
                 contraindications=json.dumps(["shoulder injury"])),

        # Leg exercises
        Exercise(name="Squat", description="Barbell squat for overall leg development",
                 muscle_group="legs", difficulty="advanced", equipment_needed=json.dumps(["barbell", "squat rack"]),
                 contraindications=json.dumps(["knee injury", "hip injury", "lower back injury"])),
        Exercise(name="Leg Press", description="Machine leg press for quadriceps development",
                 muscle_group="legs", difficulty="beginner", equipment_needed=json.dumps(["leg press machine"]),
                 contraindications=json.dumps(["knee injury"])),
        Exercise(name="Lunges", description="Walking lunges for leg development and balance",
                 muscle_group="legs", difficulty="intermediate", equipment_needed=json.dumps(["dumbbells"]),
                 contraindications=json.dumps(["knee injury", "ankle injury"])),

        # Shoulders exercises
        Exercise(name="Overhead Press", description="Barbell overhead press for shoulder development",
                 muscle_group="shoulders", difficulty="intermediate", equipment_needed=json.dumps(["barbell"]),
                 contraindications=json.dumps(["shoulder injury", "neck injury"])),
        Exercise(name="Lateral Raise", description="Dumbbell lateral raise for side deltoids",
                 muscle_group="shoulders", difficulty="beginner", equipment_needed=json.dumps(["dumbbells"]),
                 contraindications=json.dumps(["shoulder injury"])),
    # Arms exercises
    Exercise(name="Bicep Curl", description="Dumbbell bicep curl for biceps development",
             muscle_group="arms", difficulty="beginner", equipment_needed=json.dumps(["dumbbells"]),
             contraindications=json.dumps(["elbow injury", "wrist injury"])),
    Exercise(name="Tricep Extension", description="Overhead tricep extension for triceps development",
             muscle_group="arms", difficulty="beginner", equipment_needed=json.dumps(["dumbbell"]),
             contraindications=json.dumps(["elbow injury", "shoulder injury"])),
    Exercise(name="Hammer Curl", description="Dumbbell hammer curl for biceps and forearm development",
             muscle_group="arms", difficulty="beginner", equipment_needed=json.dumps(["dumbbells"]),
             contraindications=json.dumps(["elbow injury", "wrist injury"])),

        # Core exercises
    Exercise(name="Plank", description="Static plank position for core strength",
             muscle_group="abs", difficulty="beginner", equipment_needed=json.dumps(["none"]),
             contraindications=json.dumps(["shoulder injury", "lower back injury"])),
    Exercise(name="Sit-up", description="Basic sit-up for abdominal development",
             muscle_group="abs", difficulty="beginner", equipment_needed=json.dumps(["none"]),
             contraindications=json.dumps(["lower back injury", "neck injury"])),
    Exercise(name="Russian Twist", description="Seated rotation exercise for obliques",
             muscle_group="abs", difficulty="intermediate",
             equipment_needed=json.dumps(["weight plate", "medicine ball"]),
             contraindications=json.dumps(["lower back injury"])),

        # Cardio exercises
    Exercise(name="Running", description="Running outdoors or on treadmill",
             muscle_group="cardio", difficulty="intermediate", equipment_needed=json.dumps(["none", "treadmill"]),
             contraindications=json.dumps(["knee injury", "ankle injury", "hip injury"])),
    Exercise(name="Cycling", description="Cycling outdoors or on stationary bike",
             muscle_group="cardio", difficulty="beginner", equipment_needed=json.dumps(["bicycle", "stationary bike"]),
             contraindications=json.dumps(["knee injury", "hip injury"])),
    Exercise(name="Jumping Jacks", description="Basic cardio movement engaging full body",
             muscle_group="cardio", difficulty="beginner", equipment_needed=json.dumps(["none"]),
             contraindications=json.dumps(["knee injury", "ankle injury", "shoulder injury"]))
    ]

    # Add to database
    for exercise in exercises:
        db.session.add(exercise)

    db.session.commit()
    print("Database seeded with exercise options!")


@app.cli.command("seed-workout-templates")
def seed_workout_templates():
    """Seed the database with workout templates"""
    # Clear existing workout templates
    WorkoutTemplate.query.delete()

    # Get exercise IDs
    pushup = Exercise.query.filter_by(name="Push-up").first()
    bench_press = Exercise.query.filter_by(name="Bench Press").first()
    pull_up = Exercise.query.filter_by(name="Pull-up").first()
    squat = Exercise.query.filter_by(name="Squat").first()
    leg_press = Exercise.query.filter_by(name="Leg Press").first()
    overhead_press = Exercise.query.filter_by(name="Overhead Press").first()
    bicep_curl = Exercise.query.filter_by(name="Bicep Curl").first()
    plank = Exercise.query.filter_by(name="Plank").first()
    running = Exercise.query.filter_by(name="Running").first()
    cycling = Exercise.query.filter_by(name="Cycling").first()
    lunge = Exercise.query.filter_by(name="Lunges").first()
    lat_pulldown = Exercise.query.filter_by(name="Lat Pulldown").first()
    tricep_extension = Exercise.query.filter_by(name="Tricep Extension").first()
    russian_twist = Exercise.query.filter_by(name="Russian Twist").first()
    lateral_raise = Exercise.query.filter_by(name="Lateral Raise").first()

    # Sample workout templates
    templates = [
        # Beginner workouts
        WorkoutTemplate(
            name="Full Body Beginner",
            description="A full body workout for beginners focusing on the major muscle groups",
            difficulty="beginner",
            workout_type="strength",
            duration=45,
            fitness_goal="maintenance",
            exercises=json.dumps([
                {"exercise_id": pushup.id if pushup else None, "sets": 3, "reps": 10, "rest": 60},
                {"exercise_id": leg_press.id if leg_press else None, "sets": 3, "reps": 12, "rest": 60},
                {"exercise_id": lat_pulldown.id if lat_pulldown else None, "sets": 3, "reps": 10, "rest": 60},
                {"exercise_id": bicep_curl.id if bicep_curl else None, "sets": 3, "reps": 12, "rest": 60},
                {"exercise_id": plank.id if plank else None, "sets": 3, "reps": "30 seconds", "rest": 60}
            ])
        ),
        WorkoutTemplate(
            name="Beginner Cardio",
            description="A simple cardio workout for beginners",
            difficulty="beginner",
            workout_type="cardio",
            duration=30,
            fitness_goal="cutting",
            exercises=json.dumps([
                {"exercise_id": cycling.id if cycling else None, "sets": 1, "reps": "15 minutes", "rest": 60},
                {"exercise_id": running.id if running else None, "sets": 1, "reps": "10 minutes", "rest": 0}
            ])
        ),

        # Intermediate workouts
        WorkoutTemplate(
            name="Upper Body Focus",
            description="An intermediate workout focusing on upper body strength",
            difficulty="intermediate",
            workout_type="strength",
            duration=60,
            fitness_goal="bulking",
            exercises=json.dumps([
                {"exercise_id": bench_press.id if bench_press else None, "sets": 4, "reps": 8, "rest": 90},
                {"exercise_id": pull_up.id if pull_up else None, "sets": 4, "reps": 8, "rest": 90},
                {"exercise_id": overhead_press.id if overhead_press else None, "sets": 3, "reps": 10, "rest": 90},
                {"exercise_id": tricep_extension.id if tricep_extension else None, "sets": 3, "reps": 12, "rest": 60},
                {"exercise_id": bicep_curl.id if bicep_curl else None, "sets": 3, "reps": 12, "rest": 60}
            ])
        ),
        WorkoutTemplate(
            name="Lower Body Focus",
            description="An intermediate workout focusing on lower body strength",
            difficulty="intermediate",
            workout_type="strength",
            duration=60,
            fitness_goal="bulking",
            exercises=json.dumps([
                {"exercise_id": squat.id if squat else None, "sets": 4, "reps": 8, "rest": 120},
                {"exercise_id": leg_press.id if leg_press else None, "sets": 4, "reps": 10, "rest": 90},
                {"exercise_id": lunge.id if lunge else None, "sets": 3, "reps": 12, "rest": 90}
            ])
        ),

        # Advanced workouts
        WorkoutTemplate(
            name="Full Body Advanced",
            description="A challenging full body workout for advanced users",
            difficulty="advanced",
            workout_type="strength",
            duration=75,
            fitness_goal="maintenance",
            exercises=json.dumps([
                {"exercise_id": squat.id if squat else None, "sets": 5, "reps": 5, "rest": 180},
                {"exercise_id": bench_press.id if bench_press else None, "sets": 5, "reps": 5, "rest": 180},
                {"exercise_id": pull_up.id if pull_up else None, "sets": 4, "reps": "max", "rest": 120},
                {"exercise_id": overhead_press.id if overhead_press else None, "sets": 4, "reps": 8, "rest": 120},
                {"exercise_id": russian_twist.id if russian_twist else None, "sets": 3, "reps": 20, "rest": 60}
            ])
        ),

        # Specialized workouts
        WorkoutTemplate(
            name="Upper Body No Shoulders",
            description="Upper body workout avoiding shoulder exercises",
            difficulty="intermediate",
            workout_type="strength",
            duration=45,
            fitness_goal="maintenance",
            exercises=json.dumps([
                {"exercise_id": bench_press.id if bench_press else None, "sets": 4, "reps": 10, "rest": 90},
                {"exercise_id": lat_pulldown.id if lat_pulldown else None, "sets": 4, "reps": 12, "rest": 90},
                {"exercise_id": bicep_curl.id if bicep_curl else None, "sets": 3, "reps": 12, "rest": 60},
                {"exercise_id": tricep_extension.id if tricep_extension else None, "sets": 3, "reps": 12, "rest": 60},
                {"exercise_id": plank.id if plank else None, "sets": 3, "reps": "45 seconds", "rest": 60}
            ])
        ),
        WorkoutTemplate(
            name="Lower Body No Knees",
            description="Lower body workout avoiding knee-intensive exercises",
            difficulty="intermediate",
            workout_type="strength",
            duration=40,
            fitness_goal="maintenance",
            exercises=json.dumps([
                {"exercise_id": plank.id if plank else None, "sets": 4, "reps": "45 seconds", "rest": 60},
                {"exercise_id": cycling.id if cycling else None, "sets": 1, "reps": "20 minutes", "rest": 0},
                {"exercise_id": russian_twist.id if russian_twist else None, "sets": 3, "reps": 20, "rest": 60}
            ])
        ),

        # Cardio focused
        WorkoutTemplate(
            name="HIIT Cardio",
            description="High-intensity interval training for advanced cardio",
            difficulty="advanced",
            workout_type="cardio",
            duration=30,
            fitness_goal="cutting",
            exercises=json.dumps([
                {"exercise_id": running.id if running else None, "sets": 10, "reps": "30 seconds sprint/90 seconds jog",
                 "rest": 0},
                {"exercise_id": pushup.id if pushup else None, "sets": 3, "reps": "max", "rest": 60},
                {"exercise_id": squat.id if squat else None, "sets": 3, "reps": 20, "rest": 60}
            ])
        )
    ]

    # Add to database
    for template in templates:
        db.session.add(template)

    db.session.commit()
    print("Database seeded with workout templates!")


@app.route('/calendar')
@login_required
def calendar():
    """Show user's calendar with workouts and meals"""
    # Get current year and month
    today = date.today()
    year = request.args.get('year', type=int, default=today.year)
    month = request.args.get('month', type=int, default=today.month)

    # Get calendar data for the month
    calendar_data = current_user.get_calendar_data(year, month)

    return render_template('calendar.html', calendar_data=calendar_data, year=year, month=month)


@app.route('/log-workout/<int:workout_id>', methods=['GET', 'POST'])
@login_required
def log_workout(workout_id):
    """Log workout completion and details"""
    workout = Workout.query.get_or_404(workout_id)

    # Check if workout belongs to current user
    if workout.user_id != current_user.id:
        flash('Access denied', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        # Mark workout as completed
        workout.completed = True

        # Update workout details
        workout.notes = request.form.get('notes')
        workout.duration = request.form.get('duration', type=int)

        # Process exercise data
        exercises_data = []
        exercises = workout.get_exercises_completed()

        for i, exercise in enumerate(exercises):
            exercise_id = exercise.get('exercise_id')
            if exercise_id:
                sets_completed = request.form.getlist(f'sets_{i}[]')
                reps_completed = request.form.getlist(f'reps_{i}[]')
                weights_used = request.form.getlist(f'weights_{i}[]')

                # Compile exercise data
                sets_data = []
                for j in range(len(sets_completed)):
                    sets_data.append({
                        'set_number': j + 1,
                        'reps': reps_completed[j] if j < len(reps_completed) else 0,
                        'weight': weights_used[j] if j < len(weights_used) else 0
                    })

                exercises_data.append({
                    'exercise_id': exercise_id,
                    'sets': sets_data
                })

        workout.exercises_completed = json.dumps(exercises_data)
        db.session.commit()

        flash('Workout logged successfully!', 'success')
        return redirect(url_for('dashboard'))

    # For GET request, show the form
    exercises = []
    for exercise_data in workout.get_exercises_completed():
        exercise_id = exercise_data.get('exercise_id')
        if exercise_id:
            exercise = Exercise.query.get(exercise_id)
            if exercise:
                exercises.append({
                    'exercise': exercise,
                    'sets': exercise_data.get('sets', 3),
                    'reps': exercise_data.get('reps', 10)
                })

    return render_template('log_workout.html', workout=workout, exercises=exercises)


@app.route('/progress')
@login_required
def progress():
    """Show user's progress over time"""
    # Get workout statistics for the past 30 days
    workout_stats = current_user.get_workout_stats(30)

    # Get user's weight history
    # This would require a weight history model, which we don't have yet
    # For now, just use current weight and target weight
    weight_data = {
        'current': current_user.weight,
        'target': current_user.target_weight
    }

    return render_template('progress.html', workout_stats=workout_stats, weight_data=weight_data)


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """User settings page"""
    if request.method == 'POST':
        # Update password if provided
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if current_password and new_password:
            # Check if current password is correct
            if not current_user.check_password(current_password):
                flash('Current password is incorrect', 'danger')
                return redirect(url_for('settings'))

            # Check if new passwords match
            if new_password != confirm_password:
                flash('New passwords do not match', 'danger')
                return redirect(url_for('settings'))

            # Check password strength
            if not User.is_valid_password(new_password):
                flash('Password must be at least 8 characters long', 'danger')
                return redirect(url_for('settings'))

            # Update password
            current_user.set_password(new_password)
            db.session.commit()
            flash('Password updated successfully', 'success')

        # Update notification settings if we had them
        # This would be implemented when we add notification features

        return redirect(url_for('settings'))

    return render_template('settings.html')


# Error handling routes
@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500


# Development routes - only available in debug mode
if app.debug:
    @app.route('/debug/reset')
    def reset_db():
        """Reset database - ONLY FOR DEVELOPMENT"""
        db.drop_all()
        db.create_all()
        flash('Database has been reset', 'info')
        return redirect(url_for('home'))

# Main entry point
if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
    app.run(debug=True)