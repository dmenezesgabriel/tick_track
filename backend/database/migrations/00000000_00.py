import os
import peewee
from playhouse.sqlite_ext import JSONField

dir_path = os.path.dirname(__file__)
database_path = os.path.join(dir_path, os.pardir, 'database_prod.db')

# Create database
db = peewee.SqliteDatabase(database_path)


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
    name = peewee.CharField(unique=True)
    operational_system = peewee.ForeignKeyField(BaseOperationalSystem)

    class Meta:
        db_table = "Activity"


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
        BaseEvent,
        BaseOperationalSystem,
        BaseTimeEntry
    ]
    db.create_tables(tables)
