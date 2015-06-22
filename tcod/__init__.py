
import sys as _sys
import os as _os

import platform as _platform

def _get_library_crossplatform():
    bits, linkage = _platform.architecture()
    if 'win32' in _sys.platform:
        return 'lib/win32/'
    elif 'linux' in _sys.platform:
        if bits == '32bit':
            return 'lib/linux32/'
        elif bits == '64bit':
            return 'lib/linux64/'
    elif 'darwin' in _sys.platform:
        return 'lib/darwin/'
    raise ImportError('Operating system "%s" has no supported dynamic link libarary. (%s, %s)' % (_sys.platform, bits, linkage))

def _import_library_functions(lib):
    g = globals()
    for name in dir(lib):
        if name[:5] == 'TCOD_':
            g[name[5:]] = getattr(lib, name)
        elif name[:4] == 'TCOD': # short constant names
            g[name[4:]] = getattr(lib, name)
    
_os.environ['PATH'] += ';' + _os.path.join(__path__[0],
                                           _get_library_crossplatform())

try:
    import _libtcod
except ImportError:
    # get implementation specific version of _libtcod.pyd
    import importlib
    module_name = '._libtcod'
    if _platform.python_implementation() == 'CPython':
        module_name += '_cp%i%i' % _sys.version_info[:2]
        if _platform.architecture()[0] == '64bit':
            module_name += '_x64'

    _libtcod = importlib.import_module(module_name, 'tcod')

ffi = _libtcod.ffi
lib = _libtcod.lib
_import_library_functions(lib)

__all__ = [name for name in list(globals()) if name[0] != '_']