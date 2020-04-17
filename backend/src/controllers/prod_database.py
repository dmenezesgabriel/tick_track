import logging
import src.helpers.folder as folder_helper
from playhouse.sqlite_ext import SqliteExtDatabase

_logger = logging.getLogger('ProdDatabaseController')

DATABASE_PATH = folder_helper.path(['database', 'database_prod.db'])

pragmas = (
    ('cache_size', -1024 * 64),  # 64MB page-cache.
    ('journal_mode', 'wal'),  # Use WAL-mode (you should always use this!).
    ('foreign_keys', 1)  # Enforce foreign-key constraints.
)

# Pointing to database
database = SqliteExtDatabase(DATABASE_PATH, pragmas=pragmas)


def close_connection():
    """
    Close the database connection
    """
    database.close()


def initialize_db():
    """Create a database connection to the SQLite database specified by db_file
    :database: database file
    :return: Connection object or None
    """
    _logger.info('Initializing database connection')
    conn = None
    try:
        conn = database.connect()
        return conn
    except Exception as error:
        _logger.error('Error at database initialization. Error: %s', error)

    return conn
