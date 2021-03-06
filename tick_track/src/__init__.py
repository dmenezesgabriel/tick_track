import asyncio
import os

from sanic import Sanic
from sanic.response import json
from sanic_cors import CORS

import src.routes as routes
from src.config import app_config
from src.controllers import monitor as monitor_controller
from src.controllers import prod_database as prod_database_controller
from src.controllers import user_idle as user_idle_controller
from src.helpers import logger as logger_helper


def create_app(environment=os.getenv("ENVIRONMENT")):
    """
    Create ad configure the app
    """

    app = Sanic(__name__)
    CORS(app)

    app.config.from_object(app_config[environment])
    app.db = prod_database_controller.setup_db(app)

    @app.listener("before_server_start")
    async def start_db(*args, **kwargs):
        prod_database_controller.initialize_db(app)
        prod_database_controller.connect_db(app)

    @app.listener("after_server_stop")
    async def stop(*args, **kwargs):

        # Stop Activity monitor
        monitor_controller.stop()
        await asyncio.sleep(1)

        # Stop user_idle monitor
        user_idle_controller.stop()
        await asyncio.sleep(1)

        # Close database connections
        prod_database_controller.close_connection(app)
        await asyncio.sleep(1)

    # Add background tasks
    if environment != "testing":

        # Stop Activity monitor
        app.add_task(monitor_controller.run())

        # Stop user_idle monitor
        app.add_task(user_idle_controller.run())

    # Setup logger
    logger_helper.setup_logger(app)

    # Setup routes
    routes.setup_routes(app)

    @app.route("/hello")
    async def hello(request):
        return json({"hello": "Hello, World!"})

    return app


def init():
    """
    Initialize App
    """
    app = create_app()
    app.run(
        host=app.config.HOST,
        port=app.config.PORT,
        auto_reload=app.config.DEBUG,
    )
