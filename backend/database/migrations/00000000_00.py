import os
import peewee
from playhouse.sqlite_ext import JSONField
from playhouse.sqlite_ext import (
    SqliteExtDatabase, FTSModel, RowIDField, SearchField)


database_proxy = peewee.DatabaseProxy()


class BaseModel(peewee.Model):
    """Class base model"""

    class Meta:
        database = database_proxy


class BaseOperationalSystem(BaseModel):
    id = peewee.AutoField()
    name = peewee.CharField(unique=True)

    class Meta:
        table_name = "OperationalSystems"


class BaseActivity(BaseModel):
    id = peewee.AutoField()
    name = peewee.TextField(unique=True)
    operational_system = peewee.ForeignKeyField(BaseOperationalSystem)

    class Meta:
        table_name = "Activity"


class BaseActivityIndex(BaseModel, FTSModel):
    rowid = RowIDField()
    name = SearchField()

    class Meta:
        table_name = "ActivityIndex"
        # Use the porter stemming algorithm to tokenize content.
        options = {'tokenize': 'porter'}


class BaseEvent(BaseModel):
    id = peewee.AutoField()
    name = peewee.CharField()
    model = peewee.CharField(index=True)
    model_id = peewee.CharField(index=True)
    created_at = peewee.DateTimeField()
    payload = JSONField()

    class Meta:
        table_name = "Events"


class BaseTimeEntry(BaseModel):
    id = peewee.AutoField()
    event = peewee.ForeignKeyField(BaseEvent)
    start_time = peewee.DateTimeField()
    end_time = peewee.DateTimeField()
    duration = peewee.DecimalField()

    class Meta:
        table_name = "TimeEntries"


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
        BaseActivity,
        BaseActivityIndex,
        BaseEvent,
        BaseOperationalSystem,
        BaseTimeEntry
    ]
    # Set database
    db = setup_db()

    # Initialize database
    database_proxy.initialize(db)

    # Create tables
    db.create_tables(tables)
