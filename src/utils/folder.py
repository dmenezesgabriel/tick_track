import logging
import os


_logger = logging.getLogger("FolderUtils")


MAIN_FOLDER = os.path.abspath(os.path.join(os.path.dirname( __file__ ), os.pardir, os.pardir))


def folder_path(path_list):
    """Return an absolute path for the given folders structure"""
    path = MAIN_FOLDER
    for folder in path_list:
        path = os.path.join(path, folder)
    return path
