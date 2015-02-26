import sublime
import sys
from unittest import TestCase

IS_ST2 = sublime.version() < '3000'
IS_ST3 = not IS_ST2

# for testing sublime command


class test_helloworld_command(TestCase):

    def setUp(self):
        self.view = sublime.active_window().new_file()

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

    def _insert_text(self, string):
        self.view.run_command("insert", {"characters": string})


# for testing internal function
if IS_ST2:
   plugin = sys.modules["AStyleFormat"]
else:
   plugin = sys.modules["SublimeAStyleFormatter.AStyleFormat"]
