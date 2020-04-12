import peewee
from src.models.base import BaseModel
from src.models.event import BaseEvent


class BaseTimeEntry(BaseModel):
    """
    Defines the table fileds
    """
    id = peewee.PrimaryKeyField()
    event = peewee.ForeignKeyField(BaseEvent)
    start_time = peewee.DateTimeField()
    end_time = peewee.DateTimeField()
    duration = peewee.DecimalField()

    class Meta:
        def table_function(model_cls):
            """
            Names the table according to the returned value
            """
            return "TimeEntries"
