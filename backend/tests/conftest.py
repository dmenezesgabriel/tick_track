# import os
import pytest
from src import create_app
# from database import migrations


@pytest.yield_fixture
def app():
    # os.environ['DATABASE_PATH'] = 'file::memory:?cache=shared'

    app = create_app(environment='testing')

    # # Make app Migrations
    # migrations.migrate()

    yield app


@pytest.fixture
def test_cli(loop, app, sanic_client):
    return loop.run_until_complete(sanic_client(app))
