import sanic
from src import create_app


def test_create_app():
    """
    Testing app factory
    """
    app = create_app(environment='testing')
    # Function should return a Sanic instance
    assert isinstance(app, sanic.Sanic)


def test_hello_returns_200():
    """
    Testing /hello
    """
    app = create_app(environment='testing')
    # Get on /hello should return 200, ok
    request, response = app.test_client.get('/hello')
    assert response.status == 200


def test_hello_put_not_allowed():
    """
    Testing /hello
    """
    app = create_app(environment='testing')
    # Get on /hello should return 200, ok
    request, response = app.test_client.put('/hello')
    assert response.status == 405


def test_get_hello_includes_data():
    """
    Testing /hello
    """
    app = create_app(environment='testing')
    # Get on /hello should return 200, ok
    request, response = app.test_client.get('/hello')
    assert response.json.get('hello') == 'Hello, World!'
