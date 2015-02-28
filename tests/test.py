import json
import sublime
import sys
import os

from unittest import TestCase

IS_ST2 = sublime.version() < '3000'
IS_ST3 = not IS_ST2


if IS_ST2:
    plugin = sys.modules["AStyleFormat"]
else:
    plugin = sys.modules["SublimeAStyleFormatter.AStyleFormat"]


plugin_default_options = {}


def _load_default_options():
    global plugin_default_options

    with open(os.path.join(plugin.__path__, 'options_default.json')) as f:
        plugin_default_options = {
            'debug': False,
            'autoformat_on_save': False,
            'user_defined_syntax_mode_mapping': {},
            'options_c': {
                'use_only_additional_options': False,
                'additional_options_file': "",
                'additional_options': []
            },
            'options_c++': {
                'use_only_additional_options': False,
                'additional_options_file': "",
                'additional_options': []
            },
            'options_default': json.loads(f.read())
        }
_load_default_options()


class WithViewTestCaseMixin(object):
    def setUp(self):
        self.view = sublime.active_window().new_file()
        settings = self.view.settings()
        settings.set('_UNDER_UNITTEST', True)
        # Use default astyle formatter in every tests
        settings.set('AStyleFormatter', plugin_default_options)

    def tearDown(self):
        self.view.set_scratch(True)
        self.view.window().focus_view(self.view)
        self.view.window().run_command("close_file")

    def _insert_text(self, string):
        # We should disable auto indent
        backup = self.view.settings().get('auto_indent')
        try:
            self.view.settings().set('auto_indent', False)
            self.view.run_command("insert", {"characters": string})
        finally:
            self.view.settings().set('auto_indent', backup)

    def _get_text(self, region=None):
        if not region:
            region = sublime.Region(0, self.view.size())
        return self.view.substr(region)

    def _set_syntax(self, syntax):
        self.view.settings().set("syntax", syntax)


class PluginInternalFunctionTests(WithViewTestCaseMixin, TestCase):

    def setUp(self):
        super(PluginInternalFunctionTests, self).setUp()
        os.environ['_SUBLIME_ASTYLE_FORMATTER_TEST'] = '1'
        self.view.settings().set('AStyleFormatter', {'@@debug@@': '@@debug@@'})

    def tearDown(self):
        super(PluginInternalFunctionTests, self).tearDown()
        del os.environ['_SUBLIME_ASTYLE_FORMATTER_TEST']
        self.view.settings().erase('AStyleFormatter')

    def test_custom_expandvars_not_substitutable(self):
        expected = '${__NOTVALIDNOTVALID}$__NOTVALIDNOTVALID'
        actual = plugin.custom_expandvars(
            '${__NOTVALIDNOTVALID}$__NOTVALIDNOTVALID', {})
        self.assertEqual(expected, actual)

    def test_custom_expandvars_environ_only(self):
        fmt = ('This is a test: ${_SUBLIME_ASTYLE_FORMATTER_TEST}'
               '$_SUBLIME_ASTYLE_FORMATTER_TEST')
        expected = 'This is a test: 11'
        actual = plugin.custom_expandvars(fmt, {})
        self.assertEqual(expected, actual)

    def test_custom_expandvars_custom_only(self):
        fmt = 'This is a test: ${_custom_custom}$_custom_custom'
        expected = 'This is a test: 22'
        actual = plugin.custom_expandvars(fmt, {'_custom_custom': '2'})
        self.assertEqual(expected, actual)

    def test_custom_expandvars_environ_and_custom(self):
        fmt = ('This is a test: $_SUBLIME_ASTYLE_FORMATTER_TEST'
               '${_custom_custom}')
        expected = 'This is a test: 12'
        actual = plugin.custom_expandvars(fmt, {'_custom_custom': '2'})
        self.assertEqual(expected, actual)

    def test_get_settings_for_view(self):
        # Test default
        expected = '_blah_blah_blah'
        actual = plugin.get_settings_for_view(self.view, '_blah_blah_blah_key',
                                              default=expected)
        self.assertEqual(expected, actual)

        # Test general
        expected = False
        actual = plugin.get_settings_for_view(self.view, 'autoformat_on_save')
        self.assertEqual(expected, actual)

        # Test per-project setting
        expected = '@@debug@@'
        actual = plugin.get_settings_for_view(self.view, '@@debug@@')
        self.assertEqual(expected, actual)

    def test_get_syntax_for_view_plain_text(self):
        # By default, plain text
        self.assertFalse(plugin.get_syntax_for_view(self.view))

        self._set_syntax('Packages/C++/C.tmLanguage')
        self.assertEqual('c', plugin.get_syntax_for_view(self.view))

        self._set_syntax('Packages/C++/C++.tmLanguage')
        self.assertEqual('c++', plugin.get_syntax_for_view(self.view))

        self._set_syntax('Packages/Java/Java.tmLanguage')
        self.assertEqual('java', plugin.get_syntax_for_view(self.view))

        self._set_syntax('Packages/C#/C#.tmLanguage')
        self.assertEqual('cs', plugin.get_syntax_for_view(self.view))

    def test_is_supported_syntax(self):
        actual = list(map(lambda syntax: plugin.is_supported_syntax(self.view,
                                                                    syntax),
                          ['c', 'c++', 'cs', 'java']))
        expected = [True] * len(actual)
        self.assertEqual(expected, actual)


class AstyleformatCommandTests(WithViewTestCaseMixin, TestCase):
    def test_do_not_run_if_synatx_not_supported(self):
        expected = """\
int main(void) {
 int x;
   int y;
  }"""
        self._insert_text(expected)
        # Plain text
        self.view.run_command('astyleformat')

        self.assertEqual(expected, self._get_text())

    def test_run_with_c_file(self):
        self._set_syntax('Packages/C++/C.tmLanguage')
        original = """\
int main(void) {
 int x;
   int y;
  }"""
        expected = """\
int main(void) {
    int x;
    int y;
}"""
        self._insert_text(original)
        self.view.run_command('astyleformat')
        self.assertEqual(expected, self._get_text().replace('\t', '    '))
