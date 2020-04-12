import os
from sanic import Sanic
from sanic.response import json
from src.controllers import monitor as monitor_controller
from src.controllers import prod_database as prod_database_controller
import src.routes as routes
from src.config import app_config
from src.helpers import logger as logger_helper


def create_app():
    """
    Create ad configure the app
    """
    environment = os.getenv('ENVIRONMENT')
    print(environment)

    app = Sanic(__name__)

    app.config.from_object(app_config[environment])

    # Add background tasks
    app.add_task(logger_helper.setup_logger(environment))
    app.add_task(prod_database_controller.setup_database(app))
    app.add_task(monitor_controller.run())

    # Setup routes
    routes.setup_routes(app)

    @app.route('/hello')
    async def hello(request):
        return json({'hello': 'Hello, World!'})

    return app


def init():
    """
    Initialize App
    """
    app = create_app()
    app.run(
        host=app.config.HOST,
        port=app.config.PORT
    )
