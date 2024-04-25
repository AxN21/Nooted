'''
    Integrations tests for creating notes 
'''

from app import db
from app.tests.conftest import init_database
from app.models import User

def test_root(client, init_database):

    response = client.get('/')
    # redirect to the login page
    assert response.status_code == 302
    assert b'/login?' in response.data

