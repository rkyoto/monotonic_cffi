
"""
monotonic_cffi:

Just a cffi version of existing monotonic module on PyPI. See:

    https://pypi.python.org/pypi/monotonic

Tested with PyPy 2.6.1 and 4.0.0 on Windows, OSX and Ubuntu.

Copyright 2015 Matt Jones <mattjones1811@hotmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import ctypes.util
import os
import platform
import re
import sys
import time

from cffi import FFI


__all__ = ('monotonic',)


def get_os_release():
    """Get the leading numeric component of the OS release."""
    return re.match('[\d.]+', platform.release()).group(0)


def compare_versions(v1, v2):
    """Compare two version strings."""
    def normalize(v):
        return map(int, re.sub(r'(\.0+)*$', '', v).split('.'))
    return cmp(normalize(v1), normalize(v2))


try:
    monotonic = time.monotonic
except AttributeError:
    try:
        ffi = FFI()
        if sys.platform == 'darwin':  # OS X, iOS
            # using mach_absolute_time
            ffi.cdef('''
                uint64_t mach_absolute_time(void);

                typedef struct {
                    uint32_t numer;
                    uint32_t denom;
                } mach_timebase_info_data_t;

                int mach_timebase_info(mach_timebase_info_data_t *info);
            ''')
            libc = ffi.dlopen('/usr/lib/libc.dylib')

            timebase = ffi.new('mach_timebase_info_data_t *')
            libc.mach_timebase_info(timebase)
            ticks_per_second = timebase[0].numer / timebase[0].denom * 1.0e9

            def monotonic():
                """Monotonic clock, cannot go backward."""
                return libc.mach_absolute_time() / ticks_per_second

        elif (sys.platform.startswith('win32')
              or sys.platform.startswith('cygwin')):
            # Windows Vista / Windows Server 2008 or newer.
            ffi.cdef('''
                uint64_t GetTickCount64(void);
            ''')
            kernel32 = ffi.dlopen('kernel32.dll')

            def monotonic():
                """Monotonic clock, cannot go backward."""
                return kernel32.GetTickCount64() / 1000.0

        else:
            # using clock_gettime
            ffi.cdef('''
                struct timespec {
                    long tv_sec;
                    long tv_nsec;
                };

                int clock_gettime(long clk_id, struct timespec *tp);
            ''')

            try:
                so = ffi.dlopen(ctypes.util.find_library('c'))
                clock_gettime = so.clock_gettime
            except AttributeError:
                so = ffi.dlopen(ctypes.util.find_library('rt'))
                clock_gettime = so.clock_gettime

            tp = ffi.new('struct timespec *')

            if sys.platform.startswith('linux'):
                if compare_versions(get_os_release(), '2.6.28') > 0:
                    CLOCK_MONOTONIC = 4  # CLOCK_MONOTONIC_RAW
                else:
                    CLOCK_MONOTONIC = 1
            elif sys.platform.startswith('freebsd'):
                CLOCK_MONOTONIC = 4
            elif sys.platform.startswith('sunos5'):
                CLOCK_MONOTONIC = 4
            elif 'bsd' in sys.platform:
                CLOCK_MONOTONIC = 3

            def monotonic():
                """Monotonic clock, cannot go backward."""
                if clock_gettime(CLOCK_MONOTONIC, tp):
                    errno = ffi.errno
                    raise OSError(errno, os.strerror(errno))
                return tp[0].tv_sec + tp[0].tv_nsec / 1.0e9

        # Perform a sanity-check.
        if monotonic() - monotonic() > 0:
            raise ValueError('monotonic() is not monotonic!')

    except Exception:
        raise RuntimeError('no suitable implementation for this system')
