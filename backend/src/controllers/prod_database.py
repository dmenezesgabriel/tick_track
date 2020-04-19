import logging
from playhouse.sqlite_ext import SqliteExtDatabase
from src.models import base as base_model


_logger = logging.getLogger('ProdDatabaseController')


def setup_db(app):
    """
    Set the app database config
    :app: Sanic instance object
    """
    pragmas = (
        ('cache_size', -1024 * 64),  # 64MB page-cache.
        ('journal_mode', 'wal'),  # Use WAL-mode (you should always use this!).
        ('foreign_keys', 1)  # Enforce foreign-key constraints.
    )
    database_path = app.config.DATABASE
    return SqliteExtDatabase(database_path, pragmas=pragmas)


def initialize_db(app):
    """
    Set the app database proxy config
    :app: Sanic instance object
    """
    base_model.database_proxy.initialize(app.db)


def close_connection(app):
    """
    Close the database connection
    :app: Sanic instance object
    """
    app.db.close()


def connect_db(app):
    """Create a database connection to the SQLite database specified by db_file
    :app: Sanic instance object
    """
    _logger.info('Initializing database connection')
    conn = None
    try:
        conn = app.db.connect()
        return conn
    except Exception as error:
        _logger.error('Error at database initialization. Error: %s', error)

    return conn
