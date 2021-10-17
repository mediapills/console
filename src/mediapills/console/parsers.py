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
import io
import sys
import typing as t
from argparse import ArgumentParser
from argparse import SUPPRESS

from mediapills.console.abc.arguments import BaseArgument

ParserResult = t.Tuple[t.Dict[str, str], t.List[str]]


class InputParser(metaclass=abc.ABCMeta):
    """Abstract class for input parser."""

    @abc.abstractmethod
    def parse(self, argv: t.List[str]) -> ParserResult:
        """Return parsing result."""
        raise NotImplementedError

    @abc.abstractmethod
    def help(self) -> str:
        """Print a help message, including the program usage and registered arguments."""
        raise NotImplementedError


class InputArgumentsParser(InputParser):
    """CLI arguments parser."""

    def __init__(
        self, arguments: t.List[BaseArgument], description: str = "", epilog: str = "",
    ) -> None:
        """Class constructor."""
        self._args = arguments
        self._desc = description
        self._epilog = epilog
        self._parser = self.build_parser(
            self.arguments, desc=self.description, epilog=self.epilog
        )

    @classmethod
    def build_parser(
        cls,
        args: t.List[BaseArgument],
        desc: t.Optional[str] = "",
        epilog: t.Optional[str] = "",
    ) -> ArgumentParser:
        """Parser builder"""
        parser = ArgumentParser(
            prog=sys.argv[0], description=desc, epilog=epilog, add_help=False
        )
        parser = cls.extend_parser(parser=parser, args=args)
        return parser

    @staticmethod
    def extend_parser(
        parser: ArgumentParser, args: t.List[BaseArgument],
    ) -> ArgumentParser:
        """Extend parser."""
        for arg in args:
            is_dispatcher = callable(getattr(arg, "commands", None))
            is_parameter = callable(getattr(arg, "default", None))

            if is_dispatcher:
                pass  # TODO: implement CommandDispatcher sub-parser
            elif is_parameter:
                parser.add_argument(*arg.options, nargs=1)
            else:
                parser.add_argument(
                    *arg.options, action="count", default=SUPPRESS, help=arg.description
                )

        return parser

    @property
    def arguments(self) -> t.List[BaseArgument]:
        """Parser arguments getter."""
        return self._args

    @property
    def description(self) -> str:
        """Parser description getter."""
        return self._desc

    @property
    def epilog(self) -> str:
        """Parser epilog getter."""
        return self._epilog

    @property
    def parser(self) -> ArgumentParser:
        """Built-in Argument parser getter."""
        return self._parser

    def parse(self, argv: t.List[str]) -> t.Tuple[t.Dict[str, str], t.List[str]]:
        """Return parsing result."""
        args, undef = self.parser.parse_known_args(argv)
        # handle options
        return vars(args), undef

    def help(self) -> str:
        """Print a help message, including the program usage and registered arguments."""
        output = io.StringIO()
        self.parser.print_help(file=output)
        return output.getvalue()
