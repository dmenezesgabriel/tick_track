import logging
import os

import src.helpers.folder as folder_helper


def setup_logger(app):
    """
    Overwrites logger default configuration
    :app: receives a Sanic object
    """
    logs_path = f"{folder_helper.MAIN_FOLDER}/logs/"
    if not os.path.isdir(logs_path):
        os.makedirs(logs_path)

    logging.config.dictConfig(app.config.LOGGING_CONFIG)
