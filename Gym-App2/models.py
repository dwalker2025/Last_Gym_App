from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import datetime
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

    # Relationships
    restrictions = db.relationship('Restriction', backref='user', lazy=True, uselist=False,
                                   cascade="all, delete-orphan")

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

class Response(db.Model):
    __tablename__ = 'responses'

    id = db.Column(db.Integer, primary_key=True)
    last_searched = db.Column(db.DateTime)
    search = db.Column(db.String(64), unique=True, nullable=False)
    returned_data = db.Column(db.JSON,nullable = False)

    @staticmethod
    def get_time():
        return datetime.utcnow()
    
    def get_data(self):
        return self.returned_data