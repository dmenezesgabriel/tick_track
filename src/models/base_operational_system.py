from src.models.base import BaseModel
import peewee


class BaseOperationalSystem(BaseModel):
    id = peewee.PrimaryKeyField()
    name = peewee.CharField(unique=True)

    class Meta:
        def table_function(model_cls):
            return "OperationalSystems"
