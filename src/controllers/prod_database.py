import src.utils.folder as folder_utils
import logging
import peewee


_logger = logging.getLogger("StatusController")

path = ["database", "database_prod.db"]
database_path = folder_utils.folder_path(path)

# Creating database
database = peewee.SqliteDatabase(database_path)


def initialize_db():
    """Create a database connection to the SQLite database specified by db_file
    :database: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = database.connect()
        return conn
    except Exception as error:
        _logger.error(f"Error: {error}")

    return conn
