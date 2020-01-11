from src.controllers import prod_database as prod_database_controller
from peewee import Model


class BaseModel(Model):
    """Class model base"""
    # class responsible to create connection to database

    class Meta:
        # Indicates in which database the tables it will be created
        database = prod_database_controller.database
