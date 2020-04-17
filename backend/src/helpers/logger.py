import logging


def setup_logger(environment) -> logging.Logger:
    """
    Overwrites logger default configuration
    :environment: receives a string that can be 'development', 'production',
    or 'testing'
    """
    if environment == 'production':
        log_level = logging.INFO
    else:
        log_level = logging.DEBUG

    logging_format = "[%(asctime)s] %(process)d-%(levelname)s "
    logging_format += "%(module)s::%(funcName)s():l%(lineno)d: "
    logging_format += "%(message)s"

    logging.basicConfig(
        format=logging_format,
        level=log_level
    )
    logger = logging.getLogger()

    return logger
