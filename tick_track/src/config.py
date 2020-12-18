import sys

from src.helpers import folder as folder_helper


class Config(object):
    """
    Common configurations
    """

    DEBUG = False
    TESTING = False
    HOST = "0.0.0.0"
    PORT = 8000

    # Logging
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": (
                    "%(asctime)s - %(name)s [%(levelname)s]: %(message)s "
                    "%(module)s %(funcName)s %(lineno)d"
                ),
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": sys.stdout,
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "default",
                "filename": f"{folder_helper.MAIN_FOLDER}/logs/log.log",
                "maxBytes": 104857600,
                "backupCount": 3,
            },
        },
        "loggers": {
            "sanic": {"level": "DEBUG", "handlers": ["console", "file"]}
        },
        "root": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
        },
    }


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False
    DATABASE = folder_helper.path(["database", "database_prod.db"])


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    DATABASE = folder_helper.path(["database", "database_prod.db"])


class TestingConfig(Config):
    """
    Testing configurations
    """

    TESTING = True
    DATABASE = "file::memory:?cache=shared"


app_config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
