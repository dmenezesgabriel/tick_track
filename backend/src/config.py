class Config(object):
    DEBUG: bool = False
    TESTING: bool = False
    HOST: str = '0.0.0.0'
    PORT: int = 8000


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG: bool = True


class TestingConfig(Config):
    TESTING: bool = True
