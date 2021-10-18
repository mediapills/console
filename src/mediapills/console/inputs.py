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
import sys
import typing as t

from mediapills.console.abc.inputs import BaseConsoleInput
from mediapills.console.exceptions import ConsoleUnrecognizedArgumentsException
from mediapills.console.parsers import InputParser


class ConsoleInput(BaseConsoleInput):  # type: ignore
    """Command argument parser based on argparse."""

    def __init__(self, parser: InputParser):
        """Class constructor."""
        self._parser = parser
        self._argv: t.Optional[t.List[str]] = None

    @property
    def parser(self) -> InputParser:
        """Input parser getter."""
        return self._parser

    @parser.setter
    def parser(self, parser: InputParser) -> None:
        """Input parser setter."""
        self._parser = parser

    # @property
    # def command(self) -> t.Optional[str]:
    #     """Return the first argument from the raw parameters (not parsed)."""
    #     raise NotImplementedError()

    def get_arg(self, name: str) -> t.Optional[t.Union[str, int]]:
        """Return the argument value for a given argument name."""
        return self.get_args().get(name, None)

    def has_arg(self, name: str) -> bool:
        """Return true if an InputParameter object exists by name or position."""
        return self.get_arg(name) is not None

    def get_args(self) -> t.Dict[str, str]:
        """Return all the given arguments merged with the default values."""
        args, _ = self.parser.parse(self.get_argv())

        return args

    def get_argv(self) -> t.List[str]:
        """Get console arguments list"""
        if self._argv is None:
            argv = sys.argv
            argv.pop(0)
            self._argv = argv

        return self._argv

    # def bind(self) -> t.Dict[str, str]:
    #     """Binds the current Input instance with the given arguments."""
    #     raise NotImplementedError()

    def validate(self) -> None:
        """Validate arguments."""
        args, undef = self.parser.parse(self.get_argv())
        if undef:
            raise ConsoleUnrecognizedArgumentsException(undef[0])
