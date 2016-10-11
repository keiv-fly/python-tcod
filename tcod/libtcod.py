
import os as _os
import sys as _sys

import ctypes as _ctypes
import platform as _platform

from . import __path__

# add Windows dll's to PATH
if 'win32' in _sys.platform:
    _bits, _linkage = _platform.architecture()
    _os.environ['PATH'] += (';' + \
        _os.path.join(__path__[0], 'x86/' if _bits == '32bit' else 'x64'))

from . import _libtcod

_ffi = ffi = _libtcod.ffi
_lib = lib = _libtcod.lib

def _unpack_char_p(char_p):
    if char_p == _ffi.NULL:
        return ''
    return ffi.string(char_p).decode()

def _int(int_or_str):
    'return an integer where a single character string may be expected'
    if isinstance(int_or_str, str):
        return ord(int_or_str)
    if isinstance(int_or_str, bytes):
        return int_or_str[0]
    return int(int_or_str)

if _sys.version_info[0] == 2: # Python 2
    def _bytes(string):
        if isinstance(string, unicode):
            return string.encode()
        return string

    def _unicode(string):
        if not isinstance(string, unicode):
            return string.decode()
        return string

else: # Python 3
    def _bytes(string):
        if isinstance(string, str):
            return string.encode()
        return string

    def _unicode(string):
        if isinstance(string, bytes):
            return string.decode()
        return string

class _PropagateException():
    ''' context manager designed to propagate exceptions outside of a cffi
    callback context.  normally cffi suppresses the exception

    when propagate is called this class will hold onto the error until the
    control flow leaves the context, then the error will be raised

    with _PropagateException as propagate:
    # give propagate as onerror parameter for _ffi.def_extern
    '''

    def __init__(self):
        self.exc_info = None # (exception, exc_value, traceback)

    def propagate(self, *exc_info):
        ''' set an exception to be raised once this context exits

        if multiple errors are caught, only keep the first exception raised
        '''
        if not self.exc_info:
            self.exc_info = exc_info

    def __enter__(self):
        ''' once in context, only the propagate call is needed to use this
        class effectively
        '''
        return self.propagate

    def __exit__(self, type, value, traceback):
        ''' if we're holding on to an exception, raise it now

        prefers our held exception over any current raising error

        self.exc_info is reset now in case of nested manager shenanigans
        '''
        if self.exc_info:
            type, value, traceback = self.exc_info
            self.exc_info = None
        if type:
            # Python 2/3 compatible throw
            exception = type(value)
            exception.__traceback__ = traceback
            raise exception
