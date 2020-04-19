from peewee import Model, DatabaseProxy

database_proxy = DatabaseProxy()


class BaseModel(Model):
    """
    Class responsible to create database connection.
    """

    class Meta:
        # Indicates in which database the tables it will be created
        database = database_proxy
