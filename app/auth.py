from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


''' Define the blueprint for auth '''
auth = Blueprint('auth', __name__)




@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Missing data!', category='error')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home', user_id=current_user.id))
            else:
                flash('Incorrect password, try again.', category='error')
    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(username=username).first()

        if user:
            flash('Username already exists.', category='error')
        elif len(username) < 4:
            flash('Username is too short', category='error')
        elif len(password1) < 9:
            flash('Password is too short', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        else:
            new_user = User(username=username, password=generate_password_hash(password1, method='pbkdf2:sha1', salt_length=8))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created successfully!')
            return redirect(url_for('views.home', user_id=current_user.id))
    return render_template('sign_up.html', user=current_user)

