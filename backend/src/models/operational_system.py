from src.models.base import BaseModel
import peewee


class BaseOperationalSystem(BaseModel):
    """
    Defines the table fileds
    """
    id = peewee.PrimaryKeyField()
    name = peewee.CharField(unique=True)

    class Meta:
        def table_function(model_cls):
            """
            Names the table according to the returned value
            """
            return "OperationalSystems"
