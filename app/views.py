# Import necessary modules and libraries
from flask import Blueprint, jsonify, redirect, render_template, request, flash, url_for
from flask_login import login_required, current_user
from .models import Note, User
from . import db
import json


# Define the blueprint for views
views = Blueprint('views', __name__)


# Define all the endpoints
@views.route('/')
@login_required
def home():
    '''
    Endpoint for the home page

    Redirects authenticated users to the notes page
    Renders the login page for unauthenticated users
    '''

    if current_user.is_authenticated:
        return redirect(url_for('views.notes', user_id=current_user.id))

    return render_template('login.html', user=current_user)


@views.route('/notes/user-id=<int:user_id>', methods=['GET', 'POST'])
@login_required
def notes(user_id):
    '''
    Endpoint for displaying user's notes

    Renders the notes page for authenticated users
    Allows authenticated user to add new note

    Args:
        user_id (int): ID of the authenticated uer
    '''

    if current_user.id != user_id:
        return 'You are not authorized to access this page'

    if request.method == 'POST':
        title = request.form.get('title')

        if len(str(title)) <= 2:
            flash('Task must be longer than 2 character', category='error')
        else:
            try:
                new_note = Note(title=title, user_id=current_user.id)
                db.session.add(new_note)
                db.session.commit()
                flash('Note added!', category='success')
            except Exception as e:
                flash(f'error: {e}', category='error')

    notes = Note.query.filter_by(user_id=user_id).all()
    return render_template('notes.html', user=current_user, notes=notes)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    '''
    Endpoint for deleting a note

    Deletes a note from the database for the authenticated user
    '''

    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/profile/user-id=<int:user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id):
    '''
    Endpoint for the user profile page

    Allows authenticated user to change the current username
    '''

    if request.method == 'POST':
        new_username = request.form.get('new_username')

        if User.query.filter_by(username=new_username).first():
            flash('Username already exists, please choose a different one', category='error')
        elif new_username is None:
            flash('New username is required', category='error')
        elif len(str(new_username)) < 3:
            flash('Username is too short', category='error')
        elif new_username == current_user.username:
            flash('Username must be different from the last one', category='error')
        else:
            current_user.username = new_username
            db.session.commit()
            flash('Username updated successfully', category='success')
            return redirect(url_for('views.profile', user_id=current_user.id))
    
    return render_template('profile.html', user=current_user, user_id=user_id)
