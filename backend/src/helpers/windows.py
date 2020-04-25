import win32gui


def get_active_window() -> str:
    """
    Returns os active window's name
    """
    return win32gui.GetWindowText(win32gui.GetForegroundWindow())


class InactivityMonitor:
    """
    Class to check Mac operational system's user idle time.
    """
    def start(self):
        pass

    def get_idle_seconds(self):
        return None

    def close(self):
        pass
