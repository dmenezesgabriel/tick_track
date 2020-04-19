import os
import asyncio
from sanic import Sanic
from sanic.response import json
from src.controllers import monitor as monitor_controller
from src.controllers import prod_database as prod_database_controller
import src.routes as routes
from src.config import app_config
from src.helpers import logger as logger_helper


environment = os.getenv('ENVIRONMENT')


def create_app(environment=environment):
    """
    Create ad configure the app
    """

    app = Sanic(__name__)

    app.config.from_object(app_config[environment])

    # Add background tasks

    @app.listener('before_server_start')
    async def init(*args, **kwargs):
        logger_helper.setup_logger(environment)
        prod_database_controller.initialize_db()

    @app.listener('after_server_stop')
    async def stop(*args, **kwargs):
        monitor_controller.stop_monitor()
        prod_database_controller.close_connection()
        await asyncio.sleep(1)

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
        port=app.config.PORT,
        auto_reload=app.config.DEBUG
    )
