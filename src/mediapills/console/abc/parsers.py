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
import abc
import typing as t
from argparse import ArgumentParser

TParserResult = t.Tuple[t.Dict[str, str], t.List[str]]


class InputParser(metaclass=abc.ABCMeta):
    """Abstract class for input parser."""

    @abc.abstractmethod
    def parse(self, argv: t.List[str]) -> TParserResult:
        """Return parsing result."""
        raise NotImplementedError

    @abc.abstractmethod
    def help(self) -> str:
        """Print a help message, including the program usage and registered arguments."""
        raise NotImplementedError


class ConsoleArgumentParser(ArgumentParser):
    """Custom Class for parsing command line strings into Python objects."""

    def exit(  # type: ignore
        self, status: int = 0, message: t.Optional[str] = None
    ) -> None:
        """Exit from parsing execution."""
        super().exit(status=status, message=message)

    def error(self, message: str) -> None:  # type: ignore
        """Print a usage message incorporating the message to stderr and exits."""
        super().error(message=message)
