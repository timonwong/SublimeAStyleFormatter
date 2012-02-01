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

import sublime, sublime_plugin
import re
import platform
import Settings
from ctypes import *

"""
typedef void (STDCALL* fpError)(int, const char*);      // pointer to callback error handler
typedef char* (STDCALL* fpAlloc)(unsigned long);        // pointer to callback memory allocation
extern "C" EXPORT char* STDCALL AStyleMain(const char*, const char*, fpError, fpAlloc);
extern "C" EXPORT const char* STDCALL AStyleGetVersion (void);
"""
c_error_callback = WINFUNCTYPE(None, c_int, c_char_p)
c_alloc_callback = WINFUNCTYPE(c_char_p, c_ulong)

def error_callback_func(error, message):
    print "AStyleFormat: Error[%d]: %s" % (error, message)

g_buffer = None
def alloc_callback_func(size):
    buffer_type = c_char * size
    g_buffer = buffer_type()
    ptr = addressof(g_buffer)
    return ptr

def clear_buffer():
    g_buffer = None
    return

g_is_win64 = False
if platform.system() == 'Windows':
    bits, _ = platform.architecture()
    if bits == "64bit":
        g_is_win64 = True

def get_astyle_library():
    name = platform.system()
    if name == "Windows":
        if g_is_win64:
            return windll.LoadLibrary("AStyle_x64.dll")
        return windll.LoadLibrary("AStyle.dll")
    return None

def load_astyle_library():
    libc = get_astyle_library()
    # Function prototypes
    libc.AStyleMain.argtypes        = [c_char_p, c_char_p, c_error_callback, c_alloc_callback]
    libc.AStyleMain.restype         = c_char_p
    libc.AStyleGetVersion.restype   = c_char_p
    print "AStyleFormat: Loadded library: v" + libc.AStyleGetVersion()
    return libc

lib = load_astyle_library()
# Callbacks
error_callback = c_error_callback(error_callback_func)
alloc_callback = c_alloc_callback(alloc_callback_func)

language_regex = re.compile("(?<=source\.)[\w+#]+")

class AstyleformatCommand(sublime_plugin.TextCommand):
    def get_language(self):
        caret = self.view.sel()[0].a
        language = language_regex.search(self.view.scope_name(caret))
        if language == None:
            return ""
        return language.group(0).lower()

    def is_supported_language(self, lang):
        if self.view.is_scratch():
            return False
        return lang in ["c", "c++", "cs", "java"]

    def get_setting(self, key, default = None):
        return Settings.get_setting_view(self.view, key, default)

    def get_lang_setting(self, lang, default = None):
        key = "options_%s" % lang
        return Settings.get_setting_view(self.view, key, default)
    
    def get_current_line_region(self):
        # Get current selections
        selection = self.view.sel()[0]
        # Get current line
        line = self.view.line(selection)
        # Region as line begin
        line = sublime.Region(line.begin(), line.begin())
        return line

    def run(self, edit):
        lang = self.get_language()
        if not self.is_supported_language(lang): 
            return

        line = self.get_current_line_region()
        # Loading options
        lang_options        = " ".join(self.get_lang_setting(lang, []))
        options = lang_options
        # Current params
        region   = sublime.Region(0, self.view.size())
        text     = self.view.substr(region)
        text     = text.encode('utf-8')
        # Calling astyle
        formatted_code = lib.AStyleMain(text, options, error_callback, alloc_callback)
        formatted_code = formatted_code.decode('utf-8')
        # Replace to view   
        self.view.replace(edit, region, formatted_code)
        clear_buffer()
        # Restore view
        self.view.sel().clear()
        self.view.sel().add(line)
