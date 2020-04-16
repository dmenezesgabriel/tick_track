import os
import peewee
from playhouse.sqlite_ext import JSONField
from playhouse.sqlite_ext import (
    SqliteExtDatabase, FTSModel, RowIDField, SearchField)

dir_path = os.path.dirname(__file__)
database_path = os.path.join(dir_path, os.pardir, 'database_prod.db')

pragmas = (
    ('cache_size', -1024 * 64),  # 64MB page-cache.
    ('journal_mode', 'wal'),  # Use WAL-mode (you should always use this!).
    ('foreign_keys', 1)  # Enforce foreign-key constraints.
)

# Create database
db = SqliteExtDatabase(database_path, pragmas=pragmas)


class BaseModel(peewee.Model):
    """Class base model"""

    class Meta:
        database = db


class BaseOperationalSystem(BaseModel):
    id = peewee.PrimaryKeyField()
    name = peewee.CharField(unique=True)

    class Meta:
        db_table = "OperationalSystems"


class BaseActivity(BaseModel):
    id = peewee.PrimaryKeyField()
    name = peewee.TextField(unique=True)
    operational_system = peewee.ForeignKeyField(BaseOperationalSystem)

    class Meta:
        db_table = "Activity"


class BaseActivityIndex(BaseModel, FTSModel):
    rowid = RowIDField()
    name = SearchField()

    class Meta:
        db_table = "ActivityIndex"
        # Use the porter stemming algorithm to tokenize content.
        options = {'tokenize': 'porter'}


class BaseEvent(BaseModel):
    id = peewee.PrimaryKeyField()
    name = peewee.CharField()
    model = peewee.CharField(index=True)
    model_id = peewee.CharField(index=True)
    created_at = peewee.DateTimeField()
    payload = JSONField()

    class Meta:
        db_table = "Events"


class BaseTimeEntry(BaseModel):
    id = peewee.PrimaryKeyField()
    event = peewee.ForeignKeyField(BaseEvent)
    start_time = peewee.DateTimeField()
    end_time = peewee.DateTimeField()
    duration = peewee.DecimalField()

    class Meta:
        db_table = "TimeEntries"


def apply():
    tables = [
        BaseActivity,
        BaseActivityIndex,
        BaseEvent,
        BaseOperationalSystem,
        BaseTimeEntry
    ]
    db.create_tables(tables)
