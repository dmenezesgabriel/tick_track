import peewee
from src.models.base import BaseModel
from src.models.base_event import BaseEvent


class BaseTimeEntry(BaseModel):
    id = peewee.PrimaryKeyField()
    event = peewee.ForeignKeyField(BaseEvent)
    start_time = peewee.DateTimeField()
    end_time = peewee.DateTimeField()
    duration = peewee.TimeField()

    class Meta:
        def table_function(model_cls):
            return "TimeEntries"
