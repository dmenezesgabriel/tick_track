import os


MAIN_FOLDER = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))


def path(path_list):
    """
    Returns an absolute path for the given folders structure
    :path_list: receives a list type object where each element is an folder and
    it can end in a file name
    """
    path = MAIN_FOLDER
    for folder in path_list:
        path = os.path.join(path, folder)
    return path
