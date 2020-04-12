import logging
from sanic import Sanic
from sanic.response import json
from src.controllers import monitor as monitor_controller
from src.controllers import prod_database as prod_database_controller
import src.routes as routes
from src import config


logging_format = "[%(asctime)s] %(process)d-%(levelname)s "
logging_format += "%(module)s::%(funcName)s():l%(lineno)d: "
logging_format += "%(message)s"

logging.basicConfig(
    format=logging_format,
    level=logging.INFO
)
_logger = logging.getLogger('Core')


def create_app():
    """
    Create ad configure the app
    """
    app = Sanic(__name__)
    app.config.from_object(config.Config)

    # Initialize the database
    prod_database_controller.setup_database(app)

    # Setup routes
    routes.setup_routes(app)

    # Add background tasks
    app.add_task(monitor_controller.run())

    @app.route('/hello')
    async def hello(request):
        return json({'hello': 'Hello, World!'})

    return app


def init():
    """
    Initialize App
    """
    _logger.info('Initializating app')
    app = create_app()
    app.run(
        host=app.config.HOST,
        port=app.config.PORT,
        debug=app.config.DEBUG,
        auto_reload=app.config.DEBUG
    )
