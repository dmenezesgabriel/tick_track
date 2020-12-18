import peewee
from src.models.base import BaseModel
from src.models.event import Event


class TimeEntry(BaseModel):
    """
    Defines the table fileds
    """

    id = peewee.AutoField()
    event = peewee.ForeignKeyField(Event)
    start_time = peewee.DateTimeField()
    end_time = peewee.DateTimeField()
    duration = peewee.DecimalField()

    class Meta:
        def table_function(model_cls):
            """
            Names the table according to the returned value
            """
            return "TimeEntries"
