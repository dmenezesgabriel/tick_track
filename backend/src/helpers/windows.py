import win32gui


def get_active_window() -> str:
    """
    Returns os active window's name
    """
    return win32gui.GetWindowText(win32gui.GetForegroundWindow())
