from AppKit import NSWorkspace


def get_active_window() -> str:
    """
    Returns os active window's name
    """
    return (
        NSWorkspace.sharedWorkspace().activeApplication()["NSApplicationName"])
