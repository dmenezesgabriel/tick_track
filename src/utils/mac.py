from AppKit import NSWorkspace
from Foundation import *


def get_active_window():
    """
    returns the details about the window
    """
    _active_window_name = (
        NSWorkspace.sharedWorkspace().activeApplication()["NSApplicationName"])
    return _active_window_name
