from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from app.models import User
from app.forms import (
    LoginForm, RegisterForm, ProfileUpdateForm,
    PasswordChangeForm, ResetPasswordRequestForm, ResetPasswordForm
)
import json


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = RegisterForm()
    if form.validate_on_submit():
        # Check if email already exists
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered', 'danger')
            return render_template('register.html', form=form)

        # Check if username already exists
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already taken', 'danger')
            return render_template('register.html', form=form)

        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/profile', methods=['GET'])
@login_required
def profile():
    profile_form = ProfileUpdateForm(obj=current_user)

    # Set current values for goals and restrictions
    if current_user.goals:
        profile_form.goals.data = json.loads(current_user.goals)

    if current_user.restrictions:
        restrictions = json.loads(current_user.restrictions)
        profile_form.injury_areas.data = restrictions.get('injury_areas', [])
        profile_form.limited_movements.data = restrictions.get('limited_movements', [])
        profile_form.dietary_restrictions.data = restrictions.get('dietary_restrictions', [])

    password_form = PasswordChangeForm()
    return render_template('profile.html', profile_form=profile_form, password_form=password_form)


@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    form = ProfileUpdateForm()

    if form.validate_on_submit():
        # Check if email is being changed
        if form.email.data != current_user.email:
            # Check if email already exists
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user and existing_user.id != current_user.id:
                flash('Email already registered', 'danger')
                return redirect(url_for('profile'))

        # Check if username is being changed
        if form.username.data != current_user.username:
            # Check if username already exists
            existing_user = User.query.filter_by(username=form.username.data).first()
            if existing_user and existing_user.id != current_user.id:
                flash('Username already taken', 'danger')
                return redirect(url_for('profile'))

        # Update user data
        current_user.username = form.username.data
        current_user.email = form.email.data

        # Update physical information
        if form.height.data:
            current_user.change_height(form.height.data)
        if form.weight.data:
            current_user.change_weight(form.weight.data)
        if form.availability.data:
            current_user.update_availability(form.availability.data)

        # Update goals
        current_user.goals = json.dumps(form.goals.data) if form.goals.data else json.dumps([])

        # Update restrictions
        current_user.create_restrictions(
            injury_areas=form.injury_areas.data,
            limited_movements=form.limited_movements.data,
            dietary_restrictions=form.dietary_restrictions.data
        )

        # Save changes
        db.session.commit()

        flash('Profile updated successfully!', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", 'danger')

    return redirect(url_for('profile'))


@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    form = PasswordChangeForm()

    if form.validate_on_submit():
        # Verify current password
        if not current_user.check_password(form.current_password.data):
            flash('Current password is incorrect', 'danger')
            return redirect(url_for('profile'))

        # Update password
        current_user.set_password(form.new_password.data)
        db.session.commit()

        flash('Password changed successfully!', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", 'danger')

    return redirect(url_for('profile'))


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # Send password reset email (implement this function)
            send_password_reset_email(user)

        # Always show success message even if email doesn't exist (security)
        flash('Check your email for instructions to reset your password', 'info')
        return redirect(url_for('login'))

    return render_template('reset_password_request.html', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    user = User.verify_reset_password_token(token)
    if not user:
        flash('Invalid or expired reset link', 'danger')
        return redirect(url_for('login'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset', 'success')
        return redirect(url_for('login'))

    return render_template('reset_password.html', form=form)
