from src.models.base import BaseModel
import peewee


class BaseTimeEntry(BaseModel):
    id = peewee.PrimaryKeyField()
    model = peewee.CharField(index=True)
    model_id = peewee.CharField(index=True)
    start_time = peewee.CharField()
    end_time = peewee.CharField()

    class Meta:
        def table_function(model_cls):
            return "TimeEntries"
