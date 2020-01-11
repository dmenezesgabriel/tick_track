from src.models.base import BaseModel
from src.models.base_operational_system import BaseOperationalSystem
import peewee


class BaseActivity(BaseModel):
    id = peewee.PrimaryKeyField()
    name = peewee.CharField(unique=True)
    operational_system = peewee.ForeignKeyField(BaseOperationalSystem)

    class Meta:
        def table_function(model_cls):
            return "Activity"
