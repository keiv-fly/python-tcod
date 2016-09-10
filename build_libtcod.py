#!/usr/bin/env python3

import os
import sys

import platform

from cffi import FFI

module_name = 'tcod._libtcod'

def _get_library_dirs_crossplatform():
    bits, linkage = platform.architecture()
    if 'win32' in sys.platform:
        return 'src/lib/win32/'
    elif 'linux' in sys.platform:
        if bits == '32bit':
            return 'src/lib/linux32/'
        elif bits == '64bit':
            return 'src/lib/linux64/'
    elif 'darwin' in sys.platform:
        return 'src/lib/darwin/'
    raise ImportError('Operating system "%s" has no supported dynamic link libarary. (%s, %s)' % (sys.platform, bits, linkage))

def _get_libraries_crossplatform():
    bits, linkage = platform.architecture()
    if sys.platform  in ['win32', 'win64']:
        return ['libtcod-VS']
    elif 'linux' in sys.platform:
        return ['tcod']
    elif 'darwin' in sys.platform:
        return ['tcod']
    raise ImportError('Operating system "%s" has no supported dynamic link libarary. (%s, %s)' % (sys.platform, bits, linkage))

include_dirs = ['Release/src/', 'src/include/']
extra_compile_args = []

# included SDL headers are for whatever OS's don't easily come with them
if sys.platform  in ['win32', 'win64', 'darwin']:
    include_dirs += ['src/includeSDL/']

if 'darwin' in sys.platform:
    extra_compile_args += ['-Wl,-rpath=lib/darwin/']

ffi = FFI()
ffi.cdef(open('src/libtcod_cdef.h', 'r').read())
ffi.set_source(
    module_name, open('src/tdl_source.c', 'r').read(),
    include_dirs=include_dirs,
    library_dirs=[_get_library_dirs_crossplatform()],
    libraries=_get_libraries_crossplatform(),
    extra_compile_args=extra_compile_args,
)

if __name__ == "__main__":
    ffi.compile()
