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
import os
import Settings
import AStyleOptions
from AStyleLib import AStyleLib

g_language_regex = re.compile(r"(?<=source\.)[\w+#]+")
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

    def read_options_file(self, path):
        # Expand environment variables first
        fullpath = os.path.expandvars(path)
        if not os.path.exists(fullpath) or not os.path.isfile(fullpath):
            return ""
        try:
            skip_comment = re.compile(r'\s*\#')
            lines = []
            with open(fullpath, 'r') as f:
                for line in f:
                    if not skip_comment.match(line):
                        lines.append(line.strip())
            return " ".join(lines)
        except:
            return ""
        return ""

    def get_options(self, lang):
        lang_setting = self.get_lang_setting(lang, {})
        basic_option = AStyleOptions.get_basic_option_for_lang(lang) + " "

        # First, check if user will use only additional options
        if "use_only_additional_options" in lang_setting:
            use_only_additional_options = lang_setting["use_only_additional_options"]
        else:
            use_only_additional_options = False

        if "additional_options_file" in lang_setting:
            lang_options_in_file = self.read_options_file(lang_setting["additional_options_file"]) + " "
        else:
            lang_options_in_file = ""

        try:
            lang_options = " ".join(lang_setting["additional_options"]) + " " + lang_options_in_file
        except:
            lang_options = "" + lang_options_in_file

        # Skip processing other options when "use_only_additional_options" is true
        if use_only_additional_options:
            return basic_option + lang_options

        # Get default options
        default_setting = self.get_setting("options_default", {})
        # Merge lang_setting with default_setting
        setting = default_setting.copy()
        setting.update(lang_setting)
        options = AStyleOptions.process_setting(setting)
        # print ">>> SbulimeAStyleFormatter Options <<<"
        # print basic_option + lang_options + " ".join(options)
        return basic_option + lang_options + " ".join(options)

    def run(self, edit, selection_only=False):
        # Loading options
        lang = self.get_language()
        options = self.get_options(lang)
        if selection_only:
            self.run_selection_only(edit, options)
        else:
            self.run_whole_file(edit, options)
        sublime.status_message('AStyle Formatted')

    def run_selection_only(self, edit, options):
        def get_line_indentation_pos(view, point):
            line_region = view.line(point)
            pos = line_region.a
            end = line_region.b
            while pos < end:
                ch = view.substr(pos)
                if ch != ' ' and ch != '\t':
                    break
                pos += 1
            return pos

        def get_indentation_count(view, start):
            indent_count = 0
            i = start - 1
            while i > 0:
                ch = view.substr(i)
                scope = view.scope_name(i)
                # Skip preprocessors, strings, characaters and comments
                if scope.find('string.quoted') > -1 or scope.find('comment') > -1 or scope.find('preprocessor') > -1:
                    extent = view.extract_scope(i)
                    i = extent.a - 1
                    continue
                else:
                    i -= 1

                if ch == '}':
                    indent_count -= 1
                elif ch == '{':
                    indent_count += 1
            return indent_count

        view = self.view
        regions = []
        for sel in view.sel():
            start = get_line_indentation_pos(view, min(sel.a, sel.b))
            region = sublime.Region(
                view.line(start).a,  # line start of first line
                view.line(max(sel.a, sel.b)).b)  # line end of last line
            indent_count = get_indentation_count(view, start)
            # Add braces for indentation hack
            text = '{' * indent_count
            text += view.substr(region)
            # Performing astyle formatter
            formatted_code = g_astyle_lib.Format(text, options)
            if indent_count > 0:
                for _ in xrange(indent_count):
                    index = formatted_code.find('{') + 1
                    formatted_code = formatted_code[index:]
                formatted_code = re.sub(r'[ \t]*[\r\n]([^\r\n])', r'\1', formatted_code, 1)
            # Applying formatted text
            view.replace(edit, region, formatted_code)
            # Region for replaced text
            if sel.a <= sel.b:
                regions.append(sublime.Region(region.a, region.a + len(formatted_code)))
            else:
                regions.append(sublime.Region(region.a + len(formatted_code), region.a))
        view.sel().clear()
        # Add regions of formatted text
        [view.sel().add(region) for region in regions]

    def run_whole_file(self, edit, options):
        view = self.view
        bkup_region, bkup_viewport = self.get_current_region_and_viewport()
        view.set_viewport_position(tuple([0, 0]))
        # Preapare full region and its contents
        region = sublime.Region(0, view.size())
        code = view.substr(region)
        # Performing astyle formatter
        formatted_code = g_astyle_lib.Format(code, options)
        # Replace to view
        view.replace(edit, region, formatted_code)
        # "Restore" viewport
        self.set_region_and_viewport(bkup_region, bkup_viewport)

    def is_enabled(self):
        lang = self.get_language()
        return self.is_supported_language(lang)

    def get_current_region_and_viewport(self):
        view = self.view
        sel = view.sel()[0].begin()
        pos = view.rowcol(sel)
        target = view.text_point(pos[0], 0)
        return sublime.Region(target), view.viewport_position()

    def set_region_and_viewport(self, region, viewport):
        view = self.view
        view.sel().clear()
        view.sel().add(region)
        view.set_viewport_position(viewport)
