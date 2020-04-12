import re
import subprocess


def get_active_window() -> str:
    """
    Returns os active window's name
    """
    try:
        # Get Active linux window via command line command
        active_window_id_output = subprocess.check_output(
            ['xprop', '-root', '_NET_ACTIVE_WINDOW']
        )

        window_id = re.search(
            b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', active_window_id_output)

        if not window_id:
            return None
        else:
            id = window_id.group(1)

            # If window don't return id. common for not based Ubuntu os.
            if id == b'0x0':
                return b'Unmapped window'

        window_name_output = subprocess.check_output(
            ['xprop', '-id', id, 'WM_NAME'])

        window_name = re.match(
            b"WM_NAME\(\w+\) = (?P<name>.+)$", window_name_output)

        if window_name:
            return window_name.group("name").strip(b'"').decode("utf-8")
        else:
            return b'Unmapped window'
    except Exception:
        return b'Unmapped window'
