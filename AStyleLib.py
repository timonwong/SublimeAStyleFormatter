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

__all__ = ["LoadAStyleLib", "AStyleMain"]


"""
Function prototypes
typedef void (STDCALL* fpError)(int, const char*);      // pointer to callback error handler
typedef char* (STDCALL* fpAlloc)(unsigned long);        // pointer to callback memory allocation
extern "C" EXPORT char* STDCALL AStyleMain(const char*, const char*, fpError, fpAlloc);
extern "C" EXPORT const char* STDCALL AStyleGetVersion (void);
"""
# AStyle Dynamic Library
lib = None
c_alloc_callback = None
c_error_callback = None

def _load_astyle_library():
    dll = cdll
    func_type = CFUNCTYPE
    platform = sublime.platform()
    arch = sublime.arch()
    if platform == "windows":
        dll = windll
        func_type = WINFUNCTYPE
        if arch == "x64":
            libname = "AStyle_x64.dll"
        else:
            libname = "AStyle.dll"
    elif platform == "osx":
        libname = "AStyle.dynlib"
    else:
        import os
        dir = os.path.dirname(os.path.abspath(__file__))
        libname = "%s/libastyle.so" % dir
    try:
        global lib
        lib = dll.LoadLibrary(libname)
        _init_astyle_library(lib, func_type)
        return lib
    except:
        import traceback
        traceback.print_exc()
    return None

def _init_astyle_library(lib, func_type):
    # Callback
    error_callback_type = func_type(None, c_int, c_char_p)
    alloc_callback_type = func_type(c_char_p, c_ulong)
    global c_alloc_callback, c_error_callback
    c_alloc_callback = alloc_callback_type(alloc_callback)
    c_error_callback = error_callback_type(error_callback)

    # Function prototypes
    lib.AStyleMain.argtypes        = [c_char_p, c_char_p, error_callback_type, alloc_callback_type]
    lib.AStyleMain.restype         = POINTER(c_char)
    lib.AStyleGetVersion.restype   = c_char_p
    print "AStyleFormat: Loadded library: v" + lib.AStyleGetVersion()
    return lib

# Init python api, for PyMem_Malloc and PyMem_Free
PyMem_Malloc          = pythonapi.PyMem_Malloc
PyMem_Malloc.argtypes = [c_size_t]
PyMem_Malloc.restype  = c_void_p
PyMem_Free            = pythonapi.PyMem_Free
PyMem_Free.argtypes   = [c_void_p]
PyMem_Free.restype    = None

# Callback for memory allocation
def alloc_callback(size):
    return PyMem_Malloc(size)

# Callback on error
def error_callback(error, message):
    sublime.error_message("AStyleFormat: Error[%d]: %s" % (error, message))

# Entry point
def LoadAStyleLib():
    lib = _load_astyle_library()

def AStyleMain(code, options):
    code               = code.encode('utf-8')
    formatted_code_ptr = lib.AStyleMain(code, options, c_error_callback, c_alloc_callback)
    formatted_code     = cast(formatted_code_ptr, c_char_p).value
    formatted_code     = formatted_code.decode('utf-8')
    # Free buffer
    PyMem_Free(formatted_code_ptr)
    return formatted_code
