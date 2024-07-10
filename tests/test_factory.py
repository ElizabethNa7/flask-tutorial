from flaskr import create_app
# just testing that the test config is properly passed
# in general, testing the factory ensures the app can be created with different configurations and that routes behave as expected
def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'