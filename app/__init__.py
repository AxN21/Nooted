from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

# Initialize database instance
db = SQLAlchemy()
DB_NAME = 'database.db'


def create_app():

    '''
    Create and configure the Flask application

    Returns:
        app (Flask): The configured Flask application
    '''

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ahaoivhjao;vjoemPVJO' #os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' #os.getenv('DATABASE_URL')
    db.init_app(app)

    # Import and register blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    create_database(app)

    # Initialize Flask-login extension
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Define the user_loader callback for Flask-login
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


# Uncomment when in dev mode with SQLAlchemy
''' Create the database on init if it doesn't exit already '''
def create_database(app):
    if not path.exists('app/instance/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Created Database!')
