from src.models.base import BaseModel
import peewee


class BaseTimeEntry(BaseModel):
    id = peewee.PrimaryKeyField()
    model = peewee.CharField(index=True)
    model_id = peewee.CharField(index=True)
    start_time = peewee.DateTimeField()
    end_time = peewee.DateTimeField()
    duration = peewee.TimeField()

    class Meta:
        def table_function(model_cls):
            return "TimeEntries"
