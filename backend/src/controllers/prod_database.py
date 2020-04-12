import logging
import peewee
import src.helpers.folder as folder_helper


_logger = logging.getLogger('ProdDatabaseController')

DATABASE_PATH = folder_helper.path(['database', 'database_prod.db'])

# Creating database
database = peewee.SqliteDatabase(DATABASE_PATH)


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


async def setup_database(app):
    """
    Define when start or close the database
    :app: Receives a Sanic app instance
    """

    @app.listener('after_server_start')
    async def connect_to_db(*args, **kwargs):
        initialize_db()

    @app.listener('after_server_stop')
    async def disconnect_from_db(*args, **kwargs):
        close_connection()
