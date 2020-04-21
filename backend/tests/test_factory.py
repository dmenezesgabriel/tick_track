import sanic
import pytest
from src import create_app
from src.controllers import prod_database as prod_database_controller
from src.helpers import logger as logger_helper
from src import routes


@pytest.fixture(scope='function')
async def setup_db_mock_pass(monkeypatch):
    """
    Mock prod_database_controller.setup_db(app)
    """
    def new_setup_db_mock_pass(app):
        pass
    monkeypatch.setattr(
        prod_database_controller,
        'setup_db',
        new_setup_db_mock_pass
    )


@pytest.fixture(scope='function')
async def setup_logger_mock_pass(monkeypatch):
    """
    Mock logger_helper.setup_logger(environment)
    """
    def new_setup_logger_mock_pass(environment):
        pass
    monkeypatch.setattr(
        logger_helper,
        'setup_logger',
        new_setup_logger_mock_pass
    )


@pytest.fixture(scope='function')
async def setup_routes_mock_pass(monkeypatch):
    """
    Mock routes.setup_routes(app)
    """
    def new_setup_routes_mock_pass(app):
        pass
    monkeypatch.setattr(
        routes,
        'setup_routes',
        new_setup_routes_mock_pass
    )


def test_create_app(mocker, setup_routes_mock_pass):
    """
    Testing app factory
    """

    # Add spies
    mocker.spy(routes, 'setup_routes')
    mocker.spy(logger_helper, 'setup_logger')
    mocker.spy(prod_database_controller, 'setup_db')

    # Create app
    app = create_app(environment='testing')

    # Function should return a Sanic object
    assert isinstance(app, sanic.Sanic)

    # Create app should call setup functions
    assert logger_helper.setup_logger.call_count == 1
    assert routes.setup_routes.call_count == 1
    assert prod_database_controller.setup_db.call_count == 1


async def test_hello_returns_200(test_cli):
    """
    Testing /hello
    Get on /hello should return 200, ok
    """

    resp = await test_cli.get('/hello')
    assert resp.status == 200


async def test_get_hello_includes_data(test_cli):
    """
    Testing /hello
    Get on /hello should return 'Hello, World!'
    """

    resp = await test_cli.get('/hello')
    resp_json = await resp.json()
    assert resp_json.get('hello') == 'Hello, World!'
