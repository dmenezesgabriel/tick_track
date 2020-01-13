import sys
import os
import subprocess
import re


def get_active_window_raw():
    """
    returns the details about the window not just the title
    """
    root = subprocess.Popen(
        ['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE)
    stdout, stderr = root.communicate()

    m = re.search(b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout)
    if m is not None:
        window_id = m.group(1)
        window = subprocess.Popen(
            ['xprop', '-id', window_id, 'WM_NAME'], stdout=subprocess.PIPE)
        stdout, stderr = window.communicate()
    else:
        return None

    match = re.match(b"WM_NAME\(\w+\) = (?P<name>.+)$", stdout)
    if match is not None:
        ret = match.group("name").strip(b'"')
        return ret
    # If window does not have an id (experienced on Fedora)
    return b"Unmapped window"


def get_active_window():
    full_detail = get_active_window_raw().decode("utf-8")
    detail_list = None if None else full_detail
    new_window_name = detail_list
    return new_window_name
