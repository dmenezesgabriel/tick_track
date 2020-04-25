import logging
import ctypes
import ctypes.util
import re
import subprocess


_logger = logging.getLogger('Linux Helper')


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


class InactivityMonitor:
    """
    Class to check Linux operational system's user idle time.
    """

    def __init__(self):
        self._xss_available = False  # Xss library available on Linux
        self._XScreenSaverInfo_p = ctypes.POINTER(self.XScreenSaverInfo)
        self._display_p = ctypes.c_void_p
        self._xid = ctypes.c_ulong
        self._c_int_p = ctypes.POINTER(ctypes.c_int)

    def _load_library_x11(self):
        _logger.info('Loading X11 linux library')
        """
        Load Linux X11 library
        """

        try:
            # Load X11 library, if exists
            libX11path = ctypes.util.find_library('X11')
            if libX11path is None:
                print('libX11 could not be found.')
                return

            # Config lib X11
            libX11 = ctypes.cdll.LoadLibrary(libX11path)
            libX11.XOpenDisplay.restype = self._display_p
            libX11.XOpenDisplay.argtypes = ctypes.c_char_p,
            libX11.XDefaultRootWindow.restype = self._xid
            libX11.XDefaultRootWindow.argtypes = self._display_p,

            return libX11

        except Exception as error:
            print(f"Error loading library X11. {error}")

    def _load_library_xss(self):
        _logger.info('Loading Xss linux library')
        """
        Load Linux xss library
        """
        try:
            # load lib Xss, if exists
            libXsspath = ctypes.util.find_library('Xss')
            if libXsspath is None:
                print('libXss could not be found.')

            # Config lib Xss
            libXss = ctypes.cdll.LoadLibrary(libXsspath)
            libXss.XScreenSaverQueryExtension.argtypes = (
                self._display_p, self._c_int_p, self._c_int_p)
            libXss.XScreenSaverAllocInfo.restype = self._XScreenSaverInfo_p
            libXss.XScreenSaverQueryInfo.argtypes = (
                self._display_p, self._xid, self._XScreenSaverInfo_p)

            return libXss

        except Exception as error:
            print(f"Error loading library Xss. {error}")

    def start(self):
        _logger.info('Starting InactivityMonitor')
        """
        Starts activity monitor
        """

        try:
            self._libX11 = self._load_library_x11()
            self._libXss = self._load_library_xss()
            self._dpy_p = self._libX11.XOpenDisplay(None)
            if self._dpy_p is None:
                _logger.error('Could not open X Display.')
                return

            _event_basep = ctypes.c_int()
            _error_basep = ctypes.c_int()

            # Instantiate XScreenSaverQueryExtension object
            screen_saver_extension = self._libXss.XScreenSaverQueryExtension(
                    self._dpy_p,
                    ctypes.byref(_event_basep),
                    ctypes.byref(_error_basep)
            )

            # Check if XScreenSaver is available
            if screen_saver_extension == 0:
                _logger.error(
                    'XScreenSaver Extension not available on display.')
                return

            # Allocates and returns an XScreenSaverInfo structure
            # for use in calls to XScreenSaverQueryInfo
            self._xss_info_p = self._libXss.XScreenSaverAllocInfo()
            if self._xss_info_p is None:
                _logger.error('XScreenSaverAllocInfo: Out of Memory.')
                return

            # Obtains the root window for the default screen specified.
            self._rootwindow = self._libX11.XDefaultRootWindow(self._dpy_p)
            self._xss_available = True
        except Exception as error:
            _logger.error('Error on start. Error: %s', error)
            self._xss_available = False

    def get_idle_seconds(self):
        """
        Return the idle time in seconds
        """
        if not self._xss_available:
            return 0
        if self._libXss.XScreenSaverQueryInfo(self._dpy_p, self._rootwindow,
                                              self._xss_info_p) == 0:
            return 0
        else:
            return int(self._xss_info_p.contents.idle) / 1000

    def close(self):
        """
        Stops Activity Monitor
        """

        _logger.info('Closing InactivityMonitor')
        if self._xss_available:
            # You must use it to free any objects that were allocated by Xlib
            self._libX11.XFree(self._xss_info_p)
            # Code below causing segmentation fault
            # self._libX11.XCloseDisplay(self._dpy_p)
            self._xss_available = False

    class XScreenSaverInfo(ctypes.Structure):
        _fields_ = [
                # screen saver window
                ('window', ctypes.c_ulong),
                # off,on,disabled
                ('state', ctypes.c_int),
                # blanked,internal,external
                ('kind', ctypes.c_int),
                # milliseconds
                ('til_or_since', ctypes.c_ulong),
                # milliseconds
                ('idle', ctypes.c_ulong),
                # events
                ('eventMask', ctypes.c_ulong)
        ]
