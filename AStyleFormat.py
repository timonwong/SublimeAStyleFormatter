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
import sublime_plugin
import re
import Settings
from AStyleLib import AStyleLib

g_language_regex = re.compile("(?<=source\.)[\w+#]+")
g_astyle_lib = AStyleLib()


class AstyleformatCommand(sublime_plugin.TextCommand):
    def get_language(self):
        caret = self.view.sel()[0].a
        language = g_language_regex.search(self.view.scope_name(caret))
        if language == None:
            return ""
        return language.group(0).lower()

    def is_supported_language(self, lang):
        if self.view.is_scratch():
            return False
        return lang in ["c", "c++", "cs", "java"]

    def get_setting(self, key, default=None):
        return Settings.get_setting_view(self.view, key, default)

    def get_lang_setting(self, lang, default=None):
        key = "options_%s" % lang
        return Settings.get_setting_view(self.view, key, default)

    def run(self, edit):
        # Preserve line number
        preserved_line, _ = self.view.rowcol(self.view.sel()[0].begin())
        # Loading options
        lang = self.get_language()
        options = " ".join(self.get_lang_setting(lang, []))
        # Current params
        region = sublime.Region(0, self.view.size())
        code = self.view.substr(region)
        # Performing astyle formatter
        formatted_code = g_astyle_lib.Format(code, options)
        # Replace to view
        self.view.replace(edit, region, formatted_code)
        # "Restore" line
        pt = self.view.text_point(preserved_line, 0)
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(pt))
        self.view.show(pt)

    def is_enabled(self):
        lang = self.get_language()
        return self.is_supported_language(lang)
