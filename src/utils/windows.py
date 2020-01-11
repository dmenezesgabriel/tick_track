import win32gui
# import uiautomation as auto


def get_active_window():
    """
    returns the details about the window
    """
    window = win32gui.GetForegroundWindow()
    _active_window_name = win32gui.GetWindowText(window)
    return _active_window_name
