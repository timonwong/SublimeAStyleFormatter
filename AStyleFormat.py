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
import json
import re
import os
import sys

if sys.version_info < (3, 0):
    import pyastyle
    from AStyleFormatterLib import get_syntax_mode_mapping, Options
    from AStyleFormatterLib.MergeUtils import merge_code
else:
    from . import pyastyle
    from .AStyleFormatterLib import get_syntax_mode_mapping, Options
    from .AStyleFormatterLib.MergeUtils import merge_code


__file__ = os.path.normpath(os.path.abspath(__file__))
__path__ = os.path.dirname(__file__)

PLUGIN_NAME = 'SublimeAStyleFormatter'
SYNTAX_RE = re.compile(r'(?<=source\.)[\w+#]+')

with open(os.path.join(__path__, 'options_default.json')) as fp:
    OPTIONS_DEFAULT = json.load(fp)


def log(level, fmt, args):
    s = PLUGIN_NAME + ': [' + level + '] ' + (fmt.format(*args))
    print(s)


def log_debug(fmt, *args):
    log('DEBUG', fmt, args)


def load_settings():
    return sublime.load_settings(PLUGIN_NAME + '.sublime-settings')


def get_setting_for_view(view, key, default=None):
    try:
        settings = view.settings()
        sub_key = 'AStyleFormatter'
        if settings.has(sub_key):
            proj_settings = settings.get(sub_key)
            if key in proj_settings:
                return proj_settings[key]
    except:
        pass
    settings = load_settings()
    return settings.get(key, default)


def get_setting_for_active_view(key, default=None):
    return get_setting_for_view(sublime.active_window().active_view(), key, default)


def get_syntax_for_view(view):
    caret = view.sel()[0].a
    syntax = SYNTAX_RE.search(view.scope_name(caret))
    if syntax is None:
        return ''
    return syntax.group(0).lower()


def is_supported_syntax(view, syntax):
    mapping = get_setting_for_view(view, 'user_defined_syntax_mode_mapping', {})
    return syntax in get_syntax_mode_mapping(mapping)


def is_enabled_in_view(view):
    syntax = get_syntax_for_view(view)
    return is_supported_syntax(view, syntax)


class AstyleformatCommand(sublime_plugin.TextCommand):
    def _get_setting(self, key, default=None):
        return get_setting_for_view(self.view, key, default=default)

    def _get_syntax_setting(self, syntax, formatting_mode):
        key = 'options_%s' % formatting_mode
        setting = get_setting_for_view(self.view, key, default={})
        if syntax and syntax != formatting_mode:
            key = 'options_%s' % syntax
            setting_override = get_setting_for_view(self.view, key, default={})
            setting.update(setting_override)
        return setting

    def _get_default_options(self):
        options_default = OPTIONS_DEFAULT.copy()
        options_default_override = self._get_setting('options_default', default={})
        options_default.update(options_default_override)
        return options_default

    @staticmethod
    def _read_astylerc(path):
        # Expand environment variables first
        project_path = os.path.dirname(sublime.active_window().project_file_name())
        fullpath = os.path.expandvars(path).replace('$project_path', project_path)
        if not os.path.exists(fullpath) or not os.path.isfile(fullpath):
            return ''
        try:
            skip_comment = re.compile(r'\s*\#')
            lines = []
            with open(fullpath, 'r') as f:
                for line in f:
                    if not skip_comment.match(line):
                        lines.append(line.strip())
            return ' '.join(lines)
        except:
            return ''
        return ''

    @staticmethod
    def _join_options(options_list):
        options_string = ''
        first = True
        for i, o in enumerate(options_list):
            if len(o) == 0:
                continue
            if first:
                options_string += o
                first = False
            else:
                options_string += ' ' + o
        return options_string

    def get_options(self, syntax, formatting_mode):
        syntax_setting = self._get_syntax_setting(syntax, formatting_mode)
        # --mode=xxx placed first
        options_list = [Options.parse_mode_setting(formatting_mode)]

        if 'additional_options_file' in syntax_setting:
            astylerc_string = self._read_astylerc(syntax_setting['additional_options_file'])
        else:
            astylerc_string = ''

        if 'additional_options' in syntax_setting:
            additional_options = ' '.join(syntax_setting['additional_options'])
        else:
            additional_options = ''

        options_list.append(additional_options)
        options_list.append(astylerc_string)

        # Check if user will use only additional options
        # Skip processing other options when 'use_only_additional_options' is true
        if syntax_setting.get('use_only_additional_options', False):
            return self._join_options(options_list)

        # Get default options
        default_setting = self._get_default_options()
        # Merge syntax_setting with default_setting
        default_setting.update(syntax_setting)
        options = ' '.join(Options.parse_setting(default_setting))
        options_list.insert(1, options)
        return self._join_options(options_list)

    def _get_formatting_mode(self, syntax):
        mapping = get_setting_for_view(self.view,
                                       'user_defined_syntax_mode_mapping',
                                       {})
        return get_syntax_mode_mapping(mapping).get(syntax, '')

    def run(self, edit, selection_only=False):
        try:
            # Loading options
            syntax = get_syntax_for_view(self.view)
            formatting_mode = self._get_formatting_mode(syntax)
            options = self.get_options(syntax, formatting_mode)
        except Options.RangeError as e:
            sublime.error_message(str(e))
            return
        # Options ok, format now
        if selection_only:
            self.run_selection_only(edit, options)
        else:
            self.run_whole_file(edit, options)
        if self._get_setting('debug', False):
            log_debug('AStyle version: {0}', pyastyle.version())
            log_debug('Options: ' + options)
        sublime.status_message('AStyle (v%s) Formatted' % pyastyle.version())

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
                if 'string.quoted' in scope or 'comment' in scope or 'preprocessor' in scope:
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
            if indent_count > 0:
                text += '\n'
            text += view.substr(region)
            # Performing astyle formatter
            formatted_code = pyastyle.format(text, options)
            if indent_count > 0:
                for _ in range(indent_count):
                    index = formatted_code.find('{') + 1
                    formatted_code = formatted_code[index:]
                formatted_code = re.sub(r'[ \t]*\n([^\r\n])', r'\1', formatted_code, 1)
            else:
                # HACK: While no identation, a '{' will generate a blank line, so strip it.
                search = '\n{'
                if search not in text:
                    formatted_code = formatted_code.replace(search, '{', 1)
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
        region = sublime.Region(0, view.size())
        code = view.substr(region)
        # Performing astyle formatter
        formatted_code = pyastyle.format(code, options)
        # Replace to view
        _, err = merge_code(view, edit, code, formatted_code)
        if err:
            sublime.error_message('%s: Merge failure: "%s"' % (PLUGIN_NAME, err))

    def is_enabled(self):
        return is_enabled_in_view(self.view)


class PluginEventListener(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        if is_enabled_in_view(view) and get_setting_for_active_view('autoformat_on_save', default=False):
            view.run_command('astyleformat')

    def on_query_context(self, view, key, operator, operand, match_all):
        if key == 'astyleformat_is_enabled':
            return is_enabled_in_view(view)
        return None
