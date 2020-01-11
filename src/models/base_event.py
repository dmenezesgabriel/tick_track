from src.models.base import BaseModel
import peewee


class BaseEvent(BaseModel):
    id = peewee.PrimaryKeyField()
    name = peewee.CharField()
    model = peewee.CharField(index=True)
    model_id = peewee.CharField(index=True)
    created_at = peewee.DateTimeField()

    class Meta:
        def table_function(model_cls):
            return "Events"
