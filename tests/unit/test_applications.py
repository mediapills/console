# Copyright (c) 2021-2021 MediaPills Console Authors.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import unittest
from unittest.mock import Mock
from unittest.mock import patch

from mediapills.console.abc import outputs
from mediapills.console.applications import Application
from mediapills.console.outputs import ConsoleOutput


class TestApplication(unittest.TestCase):
    @patch("sys.argv", ["script_name"])
    def test_no_args_should_no_output(self) -> None:
        stdout = Mock()
        app = Application(stdout=Mock(), stderr=Mock())
        app.run()
        self.assertEqual(0, stdout.write.call_count)

    @patch("sys.argv", ["script_name", "--incorrect"])
    def test_exception_should_show_help(self) -> None:
        stdout = Mock()
        app = Application(stdout=stdout, stderr=Mock())
        with self.assertRaises(SystemExit) as e:
            app.run()
        stdout.write.assert_called_once()
        self.assertEqual(e.exception.code, 1)

    @patch("sys.argv", ["script_name"])
    def test_default_verbosity_should_be_normal(self) -> None:
        app = Application(stdout=ConsoleOutput(), stderr=Mock())
        app.run()
        self.assertFalse(app.stdout.verbosity & outputs.VERBOSITY_QUIET)
        self.assertTrue(app.stdout.verbosity & outputs.VERBOSITY_NORMAL)
        self.assertFalse(app.stdout.verbosity & outputs.VERBOSITY_VERBOSE)
        self.assertFalse(app.stdout.verbosity & outputs.VERBOSITY_DEBUG)
        self.assertFalse(app.stdout.verbosity & outputs.VERBOSITY_VERY_VERBOSE)

    @patch("sys.argv", ["script_name", "-q"])
    def test_quiet_verbosity_should_be_correct(self) -> None:
        app = Application(stdout=ConsoleOutput(), stderr=Mock())
        app.run()
        self.assertTrue(app.stdout.verbosity & outputs.VERBOSITY_QUIET)

    @patch("sys.argv", ["script_name", "-v"])
    def test_verbose_verbosity_should_be_correct(self) -> None:
        app = Application(stdout=ConsoleOutput(), stderr=Mock())
        app.run()
        self.assertTrue(app.stdout.verbosity & outputs.VERBOSITY_VERBOSE)

    @patch("sys.argv", ["script_name", "-vv"])
    def test_very_verbose_verbosity_should_be_correct(self) -> None:
        app = Application(stdout=ConsoleOutput(), stderr=Mock())
        app.run()
        self.assertTrue(app.stdout.verbosity & outputs.VERBOSITY_VERY_VERBOSE)

    @patch("sys.argv", ["script_name", "-vvv"])
    def test_debug_verbosity_should_be_correct(self) -> None:
        app = Application(stdout=ConsoleOutput(), stderr=Mock())
        app.run()
        self.assertTrue(app.stdout.verbosity & outputs.VERBOSITY_DEBUG)
