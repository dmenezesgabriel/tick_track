import src.controllers.inspector as inspector_controller
import src.controllers.prod_database as prod_database_controller
import datetime
import logging

LOG_FORMAT = "[%(asctime)s] (%(levelname)s) %(name)s: %(message)s"
logging.basicConfig(
    format=LOG_FORMAT,
    level=logging.INFO
)
_logger = logging.getLogger("Core")


def start():
    """Start core"""
    _logger.info(f"Starting Core")
    # Connect to database
    conn = prod_database_controller.initialize_db()
    _logger.info(f"Connection to database_prod: {conn}")

    # Check database tables
    tables = prod_database_controller.database.get_tables()
    _logger.info(f"Tables: {tables}")

    # Run Inspector
    inspector_controller.run()
