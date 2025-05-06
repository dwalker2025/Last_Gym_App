from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import datetime, date, timedelta
import json

from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    """User model with authentication and profile capabilities"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    streak_days = db.Column(db.Integer, default=0)

    # Gym-specific attributes
    height = db.Column(db.Integer, nullable=True)  # in cm
    weight = db.Column(db.Integer, nullable=True)  # in kg
    target_weight = db.Column(db.Float, nullable=True)  # Target weight goal
    availability = db.Column(db.Integer, nullable=True)  # hours per week
    goals = db.Column(db.String(500), nullable=True)  # JSON list of fitness goals

    # Meals based on user preferences
    dietary_preference = db.Column(db.String(50), nullable=True)  # 'vegan', 'vegetarian', 'omnivore', etc.
    fitness_goal = db.Column(db.String(50), nullable=True)  # 'bulking', 'cutting', 'maintenance'

    # Meal preferences
    preferred_proteins = db.Column(db.String(255), nullable=True)  # JSON list of preferred protein sources
    disliked_foods = db.Column(db.String(255), nullable=True)  # JSON list of disliked foods
    allergies = db.Column(db.String(255), nullable=True)  # JSON list of food allergies

    # Workout preferences
    workout_experience = db.Column(db.String(20), nullable=True)  # 'beginner', 'intermediate', 'advanced'
    workout_days_per_week = db.Column(db.Integer, nullable=True)  # Number of days per week for workouts
    workout_duration = db.Column(db.Integer, nullable=True)  # Average workout duration in minutes

    # Relationships
    restrictions = db.relationship('Restriction', backref='user', lazy=True, uselist=False,
                                   cascade="all, delete-orphan")
    workouts = db.relationship('Workout', backref='user', lazy=True, cascade="all, delete-orphan")
    meal_plans = db.relationship('UserMealPlan', backref='user', lazy=True, cascade="all, delete-orphan")

    def __init__(self, username, email, password, height=None, weight=None,
                 availability=None, goals=None, target_weight=None):
        self.username = username
        self.email = email
        self.set_password(password)
        self.height = height
        self.weight = weight
        self.target_weight = target_weight
        self.availability = availability
        self.goals = json.dumps(goals) if goals else json.dumps([])

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_goals(self):
        return json.loads(self.goals) if self.goals else []

    def get_preferred_proteins(self):
        return json.loads(self.preferred_proteins) if self.preferred_proteins else []

    def get_disliked_foods(self):
        return json.loads(self.disliked_foods) if self.disliked_foods else []

    def get_allergies(self):
        return json.loads(self.allergies) if self.allergies else []

    def add_goal(self, goal):
        goals = self.get_goals()
        if goal not in goals:
            goals.append(goal)
            self.goals = json.dumps(goals)

    def remove_goal(self, goal):
        goals = self.get_goals()
        if goal in goals:
            goals.remove(goal)
            self.goals = json.dumps(goals)

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

    def get_workout_stats(self, days=30):
        """Get workout statistics for the past X days"""
        end_date = date.today()
        start_date = end_date - timedelta(days=days)

        # Query workouts in date range
        workouts = Workout.query.filter(
            Workout.user_id == self.id,
            Workout.date >= start_date,
            Workout.date <= end_date
        ).all()

        # Group workouts by date
        workout_data = {}
        for workout in workouts:
            date_str = workout.date.strftime("%Y-%m-%d")
            if date_str not in workout_data:
                workout_data[date_str] = 0
            workout_data[date_str] += 1

        # Create a list of all dates in range and count workouts
        all_dates = []
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime("%Y-%m-%d")
            count = workout_data.get(date_str, 0)
            all_dates.append({
                'date': date_str,
                'count': count
            })
            current_date += timedelta(days=1)

        return all_dates

    def get_calendar_data(self, year=None, month=None):
        """Get user's workouts and meals for calendar display"""
        if year is None or month is None:
            today = date.today()
            year = today.year
            month = today.month

        # Get first and last day of month
        first_day = date(year, month, 1)
        if month == 12:
            last_day = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = date(year, month + 1, 1) - timedelta(days=1)

        # Query workouts in date range
        workouts = Workout.query.filter(
            Workout.user_id == self.id,
            Workout.date >= first_day,
            Workout.date <= last_day
        ).all()

        # Query meal plans in date range
        meal_plans = UserMealPlan.query.filter(
            UserMealPlan.user_id == self.id,
            UserMealPlan.date >= first_day,
            UserMealPlan.date <= last_day
        ).all()

        # Create calendar data
        calendar_data = {}

        # Add workouts to calendar
        for workout in workouts:
            date_str = workout.date.strftime("%Y-%m-%d")
            if date_str not in calendar_data:
                calendar_data[date_str] = {'workouts': [], 'meals': []}
            calendar_data[date_str]['workouts'].append({
                'id': workout.id,
                'name': workout.workout_name,
                'done': workout.completed
            })

        # Add meals to calendar
        for meal_plan in meal_plans:
            date_str = meal_plan.date.strftime("%Y-%m-%d")
            if date_str not in calendar_data:
                calendar_data[date_str] = {'workouts': [], 'meals': []}

            # Get meal details
            if meal_plan.breakfast_id:
                meal = Meal.query.get(meal_plan.breakfast_id)
                if meal:
                    calendar_data[date_str]['meals'].append({
                        'id': meal.id,
                        'name': meal.name,
                        'type': 'breakfast'
                    })

            if meal_plan.lunch_id:
                meal = Meal.query.get(meal_plan.lunch_id)
                if meal:
                    calendar_data[date_str]['meals'].append({
                        'id': meal.id,
                        'name': meal.name,
                        'type': 'lunch'
                    })

            if meal_plan.dinner_id:
                meal = Meal.query.get(meal_plan.dinner_id)
                if meal:
                    calendar_data[date_str]['meals'].append({
                        'id': meal.id,
                        'name': meal.name,
                        'type': 'dinner'
                    })

        return calendar_data

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
    def create_user(cls, username, email, password, height=None, weight=None,
                    availability=None, goals=None, target_weight=None):
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
        user = cls(
            username=username,
            email=email,
            password=password,
            height=height,
            weight=weight,
            availability=availability,
            goals=goals,
            target_weight=target_weight
        )
        return user, None


class Restriction(db.Model):
    """Model for user exercise/diet restrictions"""
    __tablename__ = 'restrictions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Physical restrictions
    injury_areas = db.Column(db.String(255), nullable=True)  # JSON list of body areas with restrictions
    limited_movements = db.Column(db.String(255), nullable=True)  # JSON list of limited movements

    # Dietary restrictions
    dietary_restrictions = db.Column(db.String(255), nullable=True)  # JSON list of foods/types to avoid

    def __init__(self, user_id, injury_areas=None, limited_movements=None, dietary_restrictions=None):
        self.user_id = user_id
        self.injury_areas = json.dumps(injury_areas) if injury_areas else json.dumps([])
        self.limited_movements = json.dumps(limited_movements) if limited_movements else json.dumps([])
        self.dietary_restrictions = json.dumps(dietary_restrictions) if dietary_restrictions else json.dumps([])

    def get_injury_areas(self):
        return json.loads(self.injury_areas)

    def get_limited_movements(self):
        return json.loads(self.limited_movements)

    def get_dietary_restrictions(self):
        return json.loads(self.dietary_restrictions)


class Meal(db.Model):
    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    calories = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Integer, nullable=False)  # in grams
    carbs = db.Column(db.Integer, nullable=False)  # in grams
    fats = db.Column(db.Integer, nullable=False)  # in grams

    # Meal category and dietary type
    meal_type = db.Column(db.String(50), nullable=False)  # breakfast, lunch, dinner, snack
    dietary_type = db.Column(db.String(50), nullable=False)  # vegan, vegetarian, omnivore
    fitness_goal = db.Column(db.String(50), nullable=False)  # bulking, cutting, maintenance

    # Additional meal attributes
    primary_protein = db.Column(db.String(50), nullable=True)  # main protein source (beef, chicken, fish, tofu, etc.)
    allergens = db.Column(db.String(255), nullable=True)  # JSON list of allergens contained in the meal

    def __repr__(self):
        return f"<Meal {self.name} - {self.meal_type}>"

    def get_allergens(self):
        return json.loads(self.allergens) if self.allergens else []

    @classmethod
    def get_personalized_meals(cls, user):
        """
        Generate a personalized meal plan for a user based on their preferences and goals
        """
        # Default values if user hasn't set preferences
        dietary_type = user.dietary_preference if user.dietary_preference else 'omnivore'
        goal = user.fitness_goal if user.fitness_goal else 'maintenance'

        # Get user restrictions
        restrictions = []
        if user.restrictions:
            restrictions = user.restrictions.get_dietary_restrictions()

        # Get allergies
        allergies = user.get_allergies() if user.allergies else []

        # Get preferred proteins
        preferred_proteins = user.get_preferred_proteins() if user.preferred_proteins else []

        # Get disliked foods
        disliked_foods = user.get_disliked_foods() if user.disliked_foods else []

        # Query base for meals matching dietary type and goal
        base_query = cls.query.filter_by(
            dietary_type=dietary_type,
            fitness_goal=goal
        )

        # Filter by meal type
        breakfast = base_query.filter_by(meal_type='breakfast').all()
        lunch = base_query.filter_by(meal_type='lunch').all()
        dinner = base_query.filter_by(meal_type='dinner').all()
        snacks = base_query.filter_by(meal_type='snack').all()

        # Filter out meals with allergies and disliked foods
        # This is a basic implementation - in a real app, you'd want more sophisticated filtering
        filtered_breakfast = []
        filtered_lunch = []
        filtered_dinner = []
        filtered_snacks = []

        # Helper function to filter meals
        def should_include_meal(meal):
            # Check allergens
            meal_allergens = meal.get_allergens()
            for allergen in allergies:
                if allergen.lower() in meal_allergens:
                    return False

            # Check if primary protein is disliked
            if meal.primary_protein and meal.primary_protein.lower() in [food.lower() for food in disliked_foods]:
                return False

            # Prioritize preferred proteins if specified
            if preferred_proteins and meal.primary_protein:
                if meal.primary_protein.lower() in [protein.lower() for protein in preferred_proteins]:
                    return True

            return True

        # Apply filters
        for meal in breakfast:
            if should_include_meal(meal):
                filtered_breakfast.append(meal)

        for meal in lunch:
            if should_include_meal(meal):
                filtered_lunch.append(meal)

        for meal in dinner:
            if should_include_meal(meal):
                filtered_dinner.append(meal)

        for meal in snacks:
            if should_include_meal(meal):
                filtered_snacks.append(meal)

        # If no specific meals found after filtering, get general ones
        if not filtered_breakfast:
            filtered_breakfast = breakfast if breakfast else cls.query.filter_by(meal_type='breakfast').limit(3).all()
        if not filtered_lunch:
            filtered_lunch = lunch if lunch else cls.query.filter_by(meal_type='lunch').limit(3).all()
        if not filtered_dinner:
            filtered_dinner = dinner if dinner else cls.query.filter_by(meal_type='dinner').limit(3).all()
        if not filtered_snacks:
            filtered_snacks = snacks if snacks else cls.query.filter_by(meal_type='snack').limit(3).all()

        return {
            'breakfast': filtered_breakfast,
            'lunch': filtered_lunch,
            'dinner': filtered_dinner,
            'snack': filtered_snacks,
            'dietary_type': dietary_type,
            'fitness_goal': goal
        }



class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    muscle_group = db.Column(db.String(50), nullable=False)  # chest, back, legs, etc.
    difficulty = db.Column(db.String(20), nullable=False)  # beginner, intermediate, advanced
    equipment_needed = db.Column(db.String(255), nullable=True)  # JSON list of required equipment
    contraindications = db.Column(db.String(255), nullable=True)  # JSON list of injury areas that shouldn't do this
    video_url = db.Column(db.String(255), nullable=True)  # Link to demonstration video

    def __repr__(self):
        return f"<Exercise {self.name} - {self.muscle_group}>"

    def get_equipment_needed(self):
        return json.loads(self.equipment_needed) if self.equipment_needed else []

    def get_contraindications(self):
        return json.loads(self.contraindications) if self.contraindications else []


class WorkoutTemplate(db.Model):
    __tablename__ = 'workout_templates'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    difficulty = db.Column(db.String(20), nullable=False)  # beginner, intermediate, advanced
    workout_type = db.Column(db.String(50), nullable=False)  # strength, cardio, flexibility, etc.
    duration = db.Column(db.Integer, nullable=False)  # in minutes
    fitness_goal = db.Column(db.String(50), nullable=False)  # bulking, cutting, maintenance

    # Store exercises as JSON with sets, reps, etc.
    exercises = db.Column(db.Text, nullable=False)  # JSON representation of exercises

    def __repr__(self):
        return f"<WorkoutTemplate {self.name} - {self.workout_type}>"

    def get_exercises(self):
        return json.loads(self.exercises) if self.exercises else []

    @classmethod
    def get_personalized_workouts(cls, user):
        """Generate personalized workout templates for a user"""
        # Default values if user hasn't set preferences
        experience = user.workout_experience if user.workout_experience else 'beginner'
        goal = user.fitness_goal if user.fitness_goal else 'maintenance'

        # Get user restrictions
        restrictions = []
        if user.restrictions:
            restrictions = user.restrictions.get_injury_areas()
            limited_movements = user.restrictions.get_limited_movements()
            if limited_movements:
                restrictions.extend(limited_movements)

        # Query workouts matching experience and goal
        workouts = cls.query.filter_by(
            difficulty=experience,
            fitness_goal=goal
        ).all()

        # Filter out workouts that target restricted areas
        suitable_workouts = []

        for workout in workouts:
            is_suitable = True

            # Check each exercise in the workout template
            for exercise_data in workout.get_exercises():
                exercise_id = exercise_data.get('exercise_id')
                if exercise_id:
                    exercise = Exercise.query.get(exercise_id)
                    if exercise:
                        # Check contraindications against user restrictions
                        contraindications = exercise.get_contraindications()
                        for restriction in restrictions:
                            if restriction.lower() in [c.lower() for c in contraindications]:
                                is_suitable = False
                                break

                if not is_suitable:
                    break

            if is_suitable:
                suitable_workouts.append(workout)

        # If no suitable workouts found, get general ones with lowest difficulty
        if not suitable_workouts:
            suitable_workouts = cls.query.filter_by(difficulty='beginner').limit(3).all()

        return suitable_workouts


class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    workout_template_id = db.Column(db.Integer, db.ForeignKey('workout_templates.id'), nullable=True)
    date = db.Column(db.Date, nullable=False, default=date.today)
    workout_name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=True)  # in minutes
    completed = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=True)

    # Store completed exercises as JSON with actual sets, reps, weights
    exercises_completed = db.Column(db.Text, nullable=True)  # JSON representation of completed exercises

    def __repr__(self):
        return f"<Workout {self.workout_name} - {self.date}>"

    def get_exercises_completed(self):
        return json.loads(self.exercises_completed) if self.exercises_completed else []


class UserMealPlan(db.Model):
    __tablename__ = 'user_meal_plans'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)

    breakfast_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=True)
    lunch_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=True)
    dinner_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=True)
    snacks = db.Column(db.Text, nullable=True)  # JSON list of snack meal IDs

    notes = db.Column(db.Text, nullable=True)

    # Relationships
    breakfast = db.relationship('Meal', foreign_keys=[breakfast_id])
    lunch = db.relationship('Meal', foreign_keys=[lunch_id])
    dinner = db.relationship('Meal', foreign_keys=[dinner_id])

    def __repr__(self):
        return f"<UserMealPlan for User {self.user_id} - {self.date}>"

    def get_snacks(self):
        return json.loads(self.snacks) if self.snacks else []
