from flask import Blueprint, jsonify, redirect, render_template, request, flash, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json


''' Define the blueprint for views '''
views = Blueprint('views', __name__)


''' Define all the endpoints  '''
@views.route('/')
@login_required
def home():
    if current_user.is_authenticated:
        return redirect(url_for('views.notes',user_id=current_user.id))
    
    return render_template('login.html', user=current_user)


@views.route('/notes/<int:user_id>', methods=['GET', 'POST'])
@login_required
def notes(user_id):
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

@views.route('/create-note/', methods=['GET', 'POST'])
@login_required
def create_note():
    if request.method == 'POST':
        title = request.form.get('title')

        if len(str(title)) < 3:
            flash('Title is too short', category='error')
        else:
            try:
                new_note = Note(title=title, user_id=current_user.id)
                db.session.add(new_note)
                db.session.commit()
                flash('Note added!', category='success')
            except Exception as e:
                flash(f'Something went wrong ,{e}', category='error')

    return redirect(url_for('views.notes', user=current_user))


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})



''' UPDATE NOTE '''
@views.route('/update-note/<int:user_id>', methods=['PATCH'])
def update_note(user_id):
    note = Note.query.get(user_id)

    if not note:
        flash('Note not found', category='error')

    data = request.json
    note.title = data.get('title', note.title)

    db.session.commit()
    flash('Note updated successfully', category='success')
