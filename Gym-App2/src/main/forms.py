from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, IntegerField, SelectField
from wtforms import BooleanField, TextAreaField, SubmitField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, NumberRange


class MultiCheckboxField(SelectMultipleField):
    """Custom field for multiple checkbox selection"""
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class LoginForm(FlaskForm):
    """User login form"""
    email = EmailField('Email', validators=[
        DataRequired(message="Email is required"),
        Email(message="Please enter a valid email address")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required")
    ])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):
    """User registration form"""
    username = StringField('Username', validators=[
        DataRequired(message="Username is required"),
        Length(min=3, max=30, message="Username must be between 3 and 30 characters")
    ])
    email = EmailField('Email', validators=[
        DataRequired(message="Email is required"),
        Email(message="Please enter a valid email address")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required"),
        Length(min=8, message="Password must be at least 8 characters long")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Please confirm your password"),
        EqualTo('password', message="Passwords must match")
    ])
    submit = SubmitField('Register')


class ProfileUpdateForm(FlaskForm):
    """User profile update form"""
    username = StringField('Username', validators=[
        DataRequired(message="Username is required"),
        Length(min=3, max=30, message="Username must be between 3 and 30 characters")
    ])
    email = EmailField('Email', validators=[
        DataRequired(message="Email is required"),
        Email(message="Please enter a valid email address")
    ])
    height = IntegerField('Height (cm)', validators=[
        Optional(),
        NumberRange(min=50, max=300, message="Please enter a valid height")
    ])
    weight = IntegerField('Weight (kg)', validators=[
        Optional(),
        NumberRange(min=20, max=500, message="Please enter a valid weight")
    ])
    availability = IntegerField('Weekly Availability (hours)', validators=[
        Optional(),
        NumberRange(min=0, max=168, message="Please enter a valid number of hours (0-168)")
    ])

    # Goal options
    goals = MultiCheckboxField('Fitness Goals', choices=[
        ('Weight Loss', 'Weight Loss'),
        ('Muscle Building', 'Muscle Building'),
        ('Flexibility', 'Flexibility'),
        ('Endurance', 'Endurance'),
        ('General Fitness', 'General Fitness')
    ])

    # Restriction options
    injury_areas = MultiCheckboxField('Injury Areas', choices=[
        ('Shoulders', 'Shoulders'),
        ('Back', 'Back'),
        ('Knees', 'Knees'),
        ('Hips', 'Hips'),
        ('Ankles', 'Ankles'),
        ('Wrists', 'Wrists')
    ])

    limited_movements = MultiCheckboxField('Limited Movements', choices=[
        ('Push-ups', 'Push-ups'),
        ('Pull-ups', 'Pull-ups'),
        ('Squats', 'Squats'),
        ('Lunges', 'Lunges'),
        ('Deadlifts', 'Deadlifts'),
        ('Overhead Press', 'Overhead Press')
    ])

    dietary_restrictions = MultiCheckboxField('Dietary Restrictions', choices=[
        ('Vegetarian', 'Vegetarian'),
        ('Vegan', 'Vegan'),
        ('Gluten-Free', 'Gluten-Free'),
        ('Dairy-Free', 'Dairy-Free'),
        ('Keto', 'Keto'),
        ('Paleo', 'Paleo')
    ])

    submit = SubmitField('Update Profile')


class PasswordChangeForm(FlaskForm):
    """Password change form"""
    current_password = PasswordField('Current Password', validators=[
        DataRequired(message="Current password is required")
    ])
    new_password = PasswordField('New Password', validators=[
        DataRequired(message="New password is required"),
        Length(min=8, message="Password must be at least 8 characters long")
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(message="Please confirm your new password"),
        EqualTo('new_password', message="Passwords must match")
    ])
    submit = SubmitField('Change Password')


class ResetPasswordRequestForm(FlaskForm):
    """Request password reset form"""
    email = EmailField('Email', validators=[
        DataRequired(message="Email is required"),
        Email(message="Please enter a valid email address")
    ])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    """Reset password form"""
    password = PasswordField('New Password', validators=[
        DataRequired(message="New password is required"),
        Length(min=8, message="Password must be at least 8 characters long")
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(message="Please confirm your new password"),
        EqualTo('password', message="Passwords must match")
    ])
    submit = SubmitField('Reset Password')

class SearchForm(FlaskForm):
    """User login form"""
    search = StringField('search', validators=[
        DataRequired(message="search is required")
    ])
    submit = SubmitField('Search')
