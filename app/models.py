# Import necessary modules and libraries
from . import db
from flask_login import UserMixin


# Create the table for the User model
class User(db.Model, UserMixin):
    '''
    Attributes:
        id (int): Primary key
        username (str): Unique
        password (str): Encripted Password
        notes (relationship): One-to-many with the notes table
    '''

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    notes = db.relationship('Note')


# Create the table for Note model
class Note(db.Model):
    '''
    Attributes:
        id (int): Primary key
        title (str): title note
        user_id (int): Foreign key referencing the id column of User table
    '''

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
