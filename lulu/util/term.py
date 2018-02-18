#!/usr/bin/env python


def get_terminal_size():
    """Get (width, height) of the current terminal."""
    try:
        # fcntl module only available on Unix
        import fcntl
        import termios
        import struct
        return struct.unpack('hh', fcntl.ioctl(1, termios.TIOCGWINSZ, '1234'))
    except Exception:
        return (40, 80)
