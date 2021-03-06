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
from mediapills.console.abc.outputs import BaseConsoleOutput


class ConsoleOutput(BaseConsoleOutput):  # type: ignore
    """Default class for all CLI output. It uses STDOUT and STDERR."""

    def write(
        self, msg: str, newline: bool = False, options: int = 0  # dead: disable
    ) -> None:
        """Write a message to the output."""
        print(msg)
        if newline:
            print("\n")

    def writeln(self, msg: str, options: int = 0) -> None:
        """Write a message to the output and adds a newline at the end."""
        self.write(msg=msg, newline=True, options=options)


class ConsoleRedOutput(ConsoleOutput):
    """Default class for all CLI output. It uses STDOUT and STDERR."""

    def write(
        self, msg: str, newline: bool = False, options: int = 0  # dead: disable
    ) -> None:
        """Write a message to the output."""
        super().write(
            msg="\033[91m" + msg + "\033[0m", newline=newline, options=options
        )
