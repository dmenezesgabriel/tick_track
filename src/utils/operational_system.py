import sys

# Operational System list
WINDOWS_OS = ["Windows", "win32", "cygwin"]
MAC_OS = ["Mac", "darwin", "os2", "os2emx"]
LINUX_OS = ["linux", "linux2"]
IOS_OS = ["ios"]


def get_os_name():
    """Return current operational system"""
    is_windows_os = sys.platform in WINDOWS_OS
    is_mac_os = sys.platform in MAC_OS
    is_linux_os = sys.platform in LINUX_OS
    is_ios_os = sys.platform in IOS_OS

    # OS check
    if is_windows_os is True:
        os_name = "windows"
    elif is_mac_os is True:
        os_name = "mac"
    elif is_linux_os is True:
        os_name = "linux"
    elif is_ios_os is True:
        os_name = "ios"
    else:
        print(f"Platform {sys.platform} is not supported")
        print(sys.version)
    return os_name
