"""
Copyright (c) 2012 Timon Wong

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sublime
from ctypes import *

__all__ = ["AStyleLib"]


def get_astyle_lib_protos():
    import os
    dll = cdll
    func_type = CFUNCTYPE
    platform = sublime.platform()
    arch = sublime.arch()
    directory = os.path.dirname(os.path.abspath(__file__))
    if platform == "windows":
        func_type = WINFUNCTYPE
        dll = windll
        libname = "%s\\AStyle%s.dll" % (directory, \
                    "" if arch != "x64" else "_x64")
    elif platform == "osx":
        libname = "%s/libastyle.dylib" % directory
    else:
        libname = "%s/libastyle.so" % directory
    return dll, libname, func_type

# Should make them public while loading
g_dll, g_libname, g_func_type = get_astyle_lib_protos()

# Init python api, for PyMem_Malloc and PyMem_Free
PyMem_Malloc = pythonapi.PyMem_Malloc
PyMem_Malloc.argtypes = [c_size_t]
PyMem_Malloc.restype = c_void_p
PyMem_Free = pythonapi.PyMem_Free
PyMem_Free.argtypes = [c_void_p]
PyMem_Free.restype = None


# Callback for memory allocation
def alloc_callback(size):
    return PyMem_Malloc(size)


# Callback on error
def error_callback(error, message):
    sublime.error_message("AStyleFormat: Error[%d]: %s" % (error, message))


class AStyleLib:
    def __init__(self):
        self.alloc_callback = None
        self.error_callback = None
        self.lib = g_dll.LoadLibrary(g_libname)
        self.__init_astyle_library()

    def __load_astyle_library(self):
        self.lib = g_dll.LoadLibrary(libname)

    def __init_astyle_library(self):
        # Callback
        error_callback_type = g_func_type(None, c_int, c_char_p)
        alloc_callback_type = g_func_type(c_char_p, c_ulong)
        self.alloc_callback = alloc_callback_type(alloc_callback)
        self.error_callback = error_callback_type(error_callback)
        # Function prototypes
        self.lib.AStyleMain.argtypes = [c_char_p, \
                                        c_char_p, \
                                        error_callback_type, \
                                        alloc_callback_type]
        self.lib.AStyleMain.restype = c_void_p

    def Format(self, code, options):
        utf8_code = code.encode('utf-8')
        # Note that c_alloc_callback will alloc memory using PyMem_Malloc
        #   so we must free them later
        formatted_code_ptr = self.lib.AStyleMain(utf8_code, \
                                                 options, \
                                                 self.error_callback, \
                                                 self.alloc_callback)
        formatted_code = cast(formatted_code_ptr, c_char_p).value
        formatted_code = formatted_code.decode('utf-8')
        # Free memory
        PyMem_Free(formatted_code_ptr)
        return formatted_code
