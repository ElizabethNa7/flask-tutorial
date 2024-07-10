# PART 9: TEST COVERAGE with Pytest
import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

# PYTEXT FIXTURES
# pytest uses fixtures by matching their function names with the names of arguments in the test functions
@pytest.fixture
def app(): # app will call the factory and pass test_config to configure the application and db for testing, instead of using your local development configs
    db_fd, db_path = tempfile.mkstemp() # tempfile.mkstemp() creates and opens a temporary file

    app = create_app({
        'TESTING': True, # TESTING tells the Flask app it's in test mode
        'DATABASE': db_path, # the DATABASE path is overridden to point to the temporary file instead of the instance folder
    })                       # after the path is set, the db tables are created and the test data is inserted. Once the test ends, the temp file is closed and removed
    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)
    yield app

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client() # client fixture calls app.test_client() with the app object created by the app fixture. Tests use the client to make requests to the app without running the server

@pytest.fixture
def runner(app):
    return app.test_cli_runner() # the runner fixture creates a runner that can call Click commands registered with the app


# AUTHENTICATION: Since for most views, a user must be logged in, you can easily have that repeated by...
# a) creating a class with methods to make POST requests to the login view, then../
class AuthActions(object):
    def __init__(self, client):
        self._client = client
    
    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'userrname': username, 'password': password}
        )
    def logout(self):
        return self._client.get('/auth/logout')
# b) using a fixture to pass those method(s) to the client for each test
@pytest.fixture
def auth(client):
    return AuthActions(client)