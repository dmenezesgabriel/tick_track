import os
import peewee
from playhouse.sqlite_ext import SqliteExtDatabase

database_proxy = peewee.DatabaseProxy()


class BaseModel(peewee.Model):
    """Class base model"""

    class Meta:
        database = database_proxy


class BaseUserIdle(BaseModel):
    id = peewee.AutoField()
    user_idle_seconds = peewee.DecimalField()

    class Meta:
        table_name = "UserIdle"


def setup_db(path=os.getenv('DATABASE_PATH')):
    pragmas = (
        ('cache_size', -1024 * 64),  # 64MB page-cache.
        ('journal_mode', 'wal'),  # Use WAL-mode (you should always use this!).
        ('foreign_keys', 1)  # Enforce foreign-key constraints.
    )

    # Create database
    return SqliteExtDatabase(path, pragmas=pragmas)


def apply():
    tables = [
        BaseUserIdle
    ]
    # Set database
    db = setup_db()

    # Initialize database
    database_proxy.initialize(db)

    # Create tables
    db.drop_tables(tables)
