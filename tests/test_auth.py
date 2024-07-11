import pytest
from flask import g, session
from flaskr.db import get_db

# test REGISTER VIEW - should successfully render on GET. With valid form data POST(ed) it should save the user's data and redirect them to the login URL
def test_register(client, app): # client.get() makes a GET request and returns the Response object from Flask
    assert client.get('/auth/register').status_code == 200 # a simple request to check for a 200 OK status_code. If rendering fails, Flask would return a 500 error code
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'} # the Response object created from client.get() converts the data dict into form data
    )
    assert response.headers["Location"] == "/auth/login" # headers have a Location header with the login URL when the register view redirects to the login view

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None

@pytest.mark.parametrize(('username', 'password', 'message'), ( # pytest.mark.parametrize tells Pytest to run the same test function with different arguments
    ('', '', b'Please enter a username.'),                         # allows to test multiple invalid input + error messages without repeating similar code
    ('a', '', b'Please enter a password.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    # make a POST request to the register endpoint with the provided username and password
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    # response.data holds the body of the HTTP response (aka all the content that the server sends back after a request), as bytes
    assert message in response.data # compare the expected message (bytes) to the response.data (also in bytes)

# test LOGIN view
def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['username'] == 'test'


@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data

def test_logout(client, auth):
    auth.login()
    with client:
        auth.logout()
        assert 'user_id' not in session