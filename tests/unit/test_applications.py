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

from mediapills.console.applications import Application


class TestApplication(unittest.TestCase):
    @patch("mediapills.console.applications.ConsoleInput")
    def test_no_args_should_no_output(self, mock_in: Mock) -> None:
        mock_in.return_value.validate.return_value = None
        mock_in.return_value.has_arg.return_value = False
        mock_out = Mock()

        app = Application(stdout=mock_out, stderr=Mock())
        app.run()

        self.assertEqual(mock_out.write.call_count, 0)

    @patch(
        "mediapills.console.applications.InputArgumentsParser.parse",
        Mock(return_value=({}, ["--option"])),
    )
    def test_exception_should_show_help(self) -> None:
        app = Application(stdout=Mock(), stderr=Mock())

        with self.assertRaises(SystemExit) as e:
            app.run()
        self.assertEqual(e.exception.code, 1)

    @patch(
        "mediapills.console.applications.InputArgumentsParser.parse",
        Mock(return_value=({}, [])),
    )
    def test_default_verbosity_should_be_normal(self) -> None:
        mock_out = Mock()

        app = Application(stdout=mock_out, stderr=Mock())
        app.run()

        self.assertEqual(mock_out.call_count, 0)

    @patch(
        "mediapills.console.applications.InputArgumentsParser.parse",
        Mock(return_value=({"quiet": 1}, [])),
    )
    def test_quiet_verbosity_should_be_correct(self) -> None:
        mock_out = Mock()

        app = Application(stdout=mock_out, stderr=Mock())
        app.run()

        mock_out.set_quiet.assert_called_once()

    @patch(
        "mediapills.console.applications.InputArgumentsParser.parse",
        Mock(return_value=({"v": 1}, [])),
    )
    def test_verbose_verbosity_should_be_correct(self) -> None:
        mock_out = Mock()

        app = Application(stdout=mock_out, stderr=Mock())
        app.run()

        mock_out.set_verbose.assert_called_once()

    @patch(
        "mediapills.console.applications.InputArgumentsParser.parse",
        Mock(return_value=({"v": 2}, [])),
    )
    def test_very_verbose_verbosity_should_be_correct(self) -> None:
        mock_out = Mock()

        app = Application(stdout=mock_out, stderr=Mock())
        app.run()

        mock_out.set_very_verbose.assert_called_once()

    @patch(
        "mediapills.console.applications.InputArgumentsParser.parse",
        Mock(return_value=({"v": 3}, [])),
    )
    def test_debug_verbosity_should_be_correct(self) -> None:
        mock_out = Mock()

        app = Application(stdout=mock_out, stderr=Mock())
        app.run()

        mock_out.set_debug.assert_called_once()

    @patch(
        "mediapills.console.applications.InputArgumentsParser.parse",
        Mock(return_value=({"help": 1}, [])),
    )
    def test_help_option_should_show_help(self) -> None:
        mock_out = Mock()
        app = Application(stdout=mock_out, stderr=Mock(), show_help=True)

        with self.assertRaises(SystemExit) as e:
            app.run()
        self.assertEqual(e.exception.code, 0)
        mock_out.write.assert_called_once()

    @patch(
        "mediapills.console.applications.InputArgumentsParser.parse",
        Mock(return_value=({"version": 1}, [])),
    )
    def test_version_option_should_show_version(self) -> None:
        mock_out = Mock()
        app = Application(
            stdout=mock_out, stderr=Mock(), version="test", show_version=True
        )

        with self.assertRaises(SystemExit) as e:
            app.run()
        self.assertEqual(e.exception.code, 0)

        mock_out.write.assert_called_once()
