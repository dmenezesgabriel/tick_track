from AppKit import NSWorkspace


def get_active_window() -> str:
    """
    Returns os active window's name
    """
    return (
        NSWorkspace.sharedWorkspace().activeApplication()["NSApplicationName"])


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
