import os
from dotenv import load_dotenv
from src.helpers import folder as folder_helper


load_dotenv(dotenv_path=folder_helper.path(['environment_variables.env']))


class Config(object):
    """
    Common configurations
    """
    DEBUG = False
    TESTING = False
    HOST = os.getenv('HOST')
    PORT = os.getenv('PORT')


class ProductionConfig(Config):
    """
    Production configurations
    """
    DEBUG = False
    DATABASE = folder_helper.path(['database', 'database_prod.db'])


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True
    DATABASE = folder_helper.path(['database', 'database_prod.db'])


class TestingConfig(Config):
    """
    Testing configurations
    """
    TESTING = True
    DATABASE = folder_helper.path(['tests', 'database_test.db'])


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
