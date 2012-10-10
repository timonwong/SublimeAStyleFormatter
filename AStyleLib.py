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


def cannot_import_ctypes_in_linux():
    import sys
    import os.path
    if sublime.platform() != "linux":
        return
    if not sublime.ok_cancel_dialog("SublimeAStyleFormatter cannot work "
        "because module 'ctypes' cannot be imported under SublimeText2\n"
        "Click \"OK\" to see how to fix it"):
        return
    sublime_app_path = os.path.dirname(sys.executable)
    script = \
"""# NOTE: Make sure SUBLIME_TEXT2_FOLDER is assigned correctly.
# Once the script is executed, you have to restart SublimeText2 to get modules work.
SUBLIME_TEXT2_FOLDER="%s"
# Download and install pythonbrew
curl -kL http://xrl.us/pythonbrewinstall | bash
source "$HOME/.pythonbrew/etc/bashrc"
pythonbrew install --configure="--enable-unicode=ucs4" 2.6
ln -s "$HOME/.pythonbrew/pythons/Python-2.6/lib/python2.6/" "${SUBLIME_TEXT2_FOLDER}/lib/python2.6"
""" % (sublime_app_path)
    # Open this script in a new view
    window = sublime.active_window()
    view = window.new_file()
    view.set_name('Workaround for importing ctypes.sh')
    view.set_scratch(True)
    edit = view.begin_edit()
    view.set_syntax_file('Packages/ShellScript/Shell-Unix-Generic.tmLanguage')
    try:
        region = sublime.Region(0, view.size())
        view.replace(edit, region, script)
        view.sel().clear()
    finally:
        view.end_edit(edit)

try:
    from ctypes import *
except ImportError:
    cannot_import_ctypes_in_linux()

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
        libname = "%s\\AStyle%s.dll" % (directory,
                                        "" if arch != "x64" else "_x64")
    elif platform == "osx":
        libname = "%s/libastyle.dylib" % directory
    else:
        libname = "%s/libastyle%s.so" % (directory,
                                         "" if arch != "x64" else "_x64")
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

    def __init_astyle_library(self):
        # Callback
        error_callback_type = g_func_type(None, c_int, c_char_p)
        alloc_callback_type = g_func_type(c_char_p, c_ulong)
        self.alloc_callback = alloc_callback_type(alloc_callback)
        self.error_callback = error_callback_type(error_callback)
        # Function prototypes
        self.lib.AStyleMain.argtypes = [c_char_p,
                                        c_char_p,
                                        error_callback_type,
                                        alloc_callback_type]
        self.lib.AStyleMain.restype = c_void_p
        # Print version info
        self.lib.AStyleGetVersion.argtypes = None
        self.lib.AStyleGetVersion.restype = c_char_p

    def Version(self):
        return self.lib.AStyleGetVersion()

    def Format(self, code, options):
        utf8_code = code.encode('utf-8')
        # Note that c_alloc_callback will alloc memory using PyMem_Malloc
        #   so we must free them later
        formatted_code_ptr = self.lib.AStyleMain(utf8_code,
                                                 options,
                                                 self.error_callback,
                                                 self.alloc_callback)
        formatted_code = cast(formatted_code_ptr, c_char_p).value
        formatted_code = formatted_code.decode('utf-8')
        # Free memory
        PyMem_Free(formatted_code_ptr)
        return formatted_code
