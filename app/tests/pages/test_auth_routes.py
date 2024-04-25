from app.models import User
from app import db
from app.tests.conftest import init_database


'''
    Tests for the user registration

'''

def test_sign_up_success(client, init_database):
    # This tests the successful user registration
    response = client.post('/sign-up', data={'username': 'testuser', 'password1': '123456789', 'password2': '123456789'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Account created successfully!' in response.data

    # and check that the user has been added to the database
    user = User.query.filter_by(username='testuser').first()
    assert user is not None

def test_sign_up_username_exists(client, init_database):
    # Test registetion with an existing username
    existing_username = User(username='testuserexists', password='passwordtest')
    db.session.add(existing_username)
    db.session.commit()

    response = client.post('/sign-up', data={'username': 'testuserexists', 'password1': '123456789', 'password2': '123456789'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Username already exists.' in response.data


'''
    Tests for the user login

'''
def test_login_success(client, init_database):
    # This tests the successful user login

    # Add a test user to the database
    existing_user = User(username='testuser', password='testpassword')
    db.session.add(existing_user)
    db.session.commit()


    response = client.post('/login', data={'username': 'testuser', 'password': 'testpassword'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'<title>Login</title>' in response.data


'''
    Tests for the logout

'''
def test_logout_success(client, init_database):
    # This tests the successful logout
    
    response = client.get('/logout')

    # 302 status code -> after successful logout the user is redirected to the login page
    assert response.status_code == 302
    assert b'redirected automatically' in response.data
    assert b'/login?' in response.data

