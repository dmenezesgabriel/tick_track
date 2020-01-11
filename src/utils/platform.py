import sys

# Operational System list
WINDOWS_OS = ["Windows", "win32", "cygwin"]
MAC_OS = ["Mac", "darwin", "os2", "os2emx"]
LINUX_OS = ["linux", "linux2"]


def get_os_name():
    """Return current operational system"""
    is_windows_os = sys.platform in WINDOWS_OS
    is_mac_os = sys.platform in MAC_OS
    is_linux_os = sys.platform in LINUX_OS

    # OS check
    if is_windows_os is True:
        os_name = "windows"
    elif is_mac_os is True:
        os_name = "mac"
    elif is_linux_os is True:
        os_name = "linux"
    else:
        print(f"Platform {sys.platform} is not supported")
        print(sys.version)
    return os_name


def import_os(os_name):
    """ Make right import for respective OS"""
    exec(
        f"import src.utils.{os_name}",
        globals()
    )


def os_get_active_window(os_name):
    "Retrieve the current window for respective os"
    return eval(f"src.utils.{os_name}.get_active_window()")


# os_name = get_os_name()
# import_os(os_name)
# print(os_get_active_window(os_name))
