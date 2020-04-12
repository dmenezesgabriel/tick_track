from src.models.base import BaseModel
from src.models.operational_system import BaseOperationalSystem
import peewee


class BaseActivity(BaseModel):
    """
    Defines the table fileds
    """
    id = peewee.PrimaryKeyField()
    name = peewee.CharField(unique=True)
    operational_system = peewee.ForeignKeyField(BaseOperationalSystem)

    class Meta:
        def table_function(model_cls):
            """
            Names the table according to the returned value
            """
            return "Activity"
