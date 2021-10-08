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
import typing as t

from mediapills.console.commands import BaseCommand


class CommandInvoker:  # dead: disable
    """Application Invoker abstraction.."""

    def __init__(self) -> None:  # dead: disable
        """Class constructor."""
        self._command = {}  # type: t.Dict[str, BaseCommand]

    def register(self, name: str, command: BaseCommand) -> None:  # dead: disable
        """Register a new command."""
        # TODO: already exists
        self._command[name] = command

    def has_command(self, name: str) -> bool:  # dead: disable
        """Return true if an command object by name exists."""
        return name in self._command

    def execute(self, name: str) -> None:  # dead: disable
        """Execute the command by name."""
        raise NotImplementedError()
