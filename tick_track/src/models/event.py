import peewee
from playhouse.sqlite_ext import JSONField
from src.models.base import BaseModel


class BaseEvent(BaseModel):
    """
    Defines the table fileds
    """
    id = peewee.AutoField()
    name = peewee.CharField()
    model = peewee.CharField(index=True)
    model_id = peewee.CharField(index=True)
    created_at = peewee.DateTimeField()
    payload = JSONField()

    class Meta:
        def table_function(model_cls):
            """
            Names the table according to the returned value
            """
            return "Events"
