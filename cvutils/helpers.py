import os
import sys

EMPTY_VALUES = ['', None, [], (), u'']

ACCEPTED_IMAGE_MIMETYPES = [
    'image/gif',
    'image/jpeg',
    'image/pjpeg',
    'image/png',
    'image/svg+xml',
    'image/tiff'

]


def which(cmd):
    """
    Similar to the 'which' command in *nix, this function searches the system PATH to see if the provided 'cmd' is
    found. If so, it returns the absolute path.
    """

    found_path = None
    paths = os.environ.get("PATH").split(":")
    for path in paths:

        if path in EMPTY_VALUES:
            continue

        if cmd in os.listdir(path):
            found_path = os.path.join(path, cmd)
            return found_path

    return found_path

def is_installed(cmd):
    """
    Similar to the 'which' command in *nix, this function searches the system PATH to see if the provided 'cmd' is
    found. If so, it returns True, else returns False.
    """

    found = False
    paths = os.environ.get("PATH").split(":")
    for path in paths:

        if path in EMPTY_VALUES:
            continue

        if cmd in os.listdir(path):
            found_path = os.path.join(path, cmd)
            return True

    return found

def verify_installed(cmd):

    if type(cmd) == str:
        if not is_installed(cmd):
            raise IOError("'%s' is not installed in your system. Please install before continuing." % cmd)

    if type(cmd) in [list, tuple]:
        for c in cmd:
            if not is_installed(c):
                raise IOError("'%s' is not installed in your system. Please install before continuing." % c)