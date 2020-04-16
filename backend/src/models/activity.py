import peewee
from playhouse.sqlite_ext import (FTSModel, RowIDField, SearchField)
from src.models.base import BaseModel
from src.models.operational_system import BaseOperationalSystem


class BaseActivity(BaseModel):
    """
    Defines the table fileds
    """
    id = peewee.PrimaryKeyField()
    name = peewee.TextField(unique=True)
    operational_system = peewee.ForeignKeyField(BaseOperationalSystem)

    class Meta:
        def table_function(model_cls):
            """
            Names the table according to the returned value
            """
            return "Activity"


class BaseActivityIndex(BaseModel, FTSModel):
    rowid = RowIDField()
    name = SearchField()

    class Meta:
        # Use the porter stemming algorithm to tokenize content.
        options = {'tokenize': 'porter'}

        def table_function(model_cls):
            """
            Names the table according to the returned value
            """
            return "ActivityIndex"
