from src.helpers import folder as folder_helper


class Config(object):
    """
    Common configurations
    """
    DEBUG = False
    TESTING = False
    HOST = "0.0.0.0"
    PORT = 8000


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
    DATABASE = 'file::memory:?cache=shared'


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
