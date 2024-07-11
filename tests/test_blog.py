# all the blog views use the auth fixture written earlier. When auth.login() and the subsequent requests from the client will be logged in as the test user
import pytest
from flaskr.db import get_db

# checking that the index (main) view displays the expected test data
def test_index(client, auth): 
    response = client.get('/')
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'test title' in response.data
    assert b'by test on 2018-01-01' in response.data
    assert b'test\nbody' in response.data
    assert b'href="/1/update"' in response.data # this checks that if logged in as the author you have a link to Edit the post


@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
    '/1/delete',
))
def test_login_required(client, path): # user must be logged in to access the create, update, and delete views
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"

def test_author_required(app, client, auth):
    # change the post author to another user
    with app.app_context():
        db = get_db()
        db.execute('UPDATE post SET author_id = 2 WHERE id = 1')
        db.commit()
    auth.login()
    # user cannot modify other's post(s)
    assert client.post('/1/update').status_code == 403 # 403 Forbidden status
    assert client.post('/1/delete').status_code == 403
    assert b'href="/1/update"' not in client.get('/').data

@pytest.mark.parametrize('path', (
    '/2/update',
    '/2/delete',
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404 # if post with the given id DNE, return 404 NOT FOUND


def test_create(client, auth, app):
    auth.login()
    assert client.get('/create').status_code == 200 # create and update views return a 200 OK status for a GET request
    client.post('/create', data={'title': 'created', 'body': ''})

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM post').fetchone()[0]
        assert count == 2

def test_update(client, auth, app):
    auth.login()
    assert client.get('/1/update').status_code == 200
    client.post('/1/update', data={'title': 'updated', 'body': ''})

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post['title'] == 'updated'
    
@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
))
def test_create_update_validate(client, auth, path):
     auth.login()
     response = client.post(path, data={'title': '', 'body': ''})
     assert b'A title is required.' in response.data

def test_delete(client, auth, app):
    auth.login()
    response = client.post('/1/delete')
    assert response.headers["Location"] == "/"
    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id - 1').fetchone()
        assert post is None