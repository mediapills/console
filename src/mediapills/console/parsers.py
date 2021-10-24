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
import io
import sys
import typing as t
from argparse import ArgumentParser
from argparse import SUPPRESS

from mediapills.console.abc.arguments import BaseArgument
from mediapills.console.abc.parsers import ConsoleArgumentParser
from mediapills.console.abc.parsers import InputParser


class InputArgumentsParser(InputParser):  # type: ignore
    """CLI arguments parser."""

    def __init__(
        self, arguments: t.List[BaseArgument], description: str = "", epilog: str = "",
    ) -> None:
        """Class constructor."""
        self._args = arguments
        self._desc = description
        self._epilog = epilog
        self._parser: t.Optional[ConsoleArgumentParser] = None

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

    @classmethod
    def extend_parser(
        cls,
        parser: ArgumentParser,
        args: t.List[BaseArgument],
        subparsers: t.Any = None,
    ) -> t.Tuple[ArgumentParser, t.Any]:
        """Extend parser."""
        for arg in args:
            is_command = callable(getattr(arg, "execute", None))
            is_parameter = callable(getattr(arg, "default", None))

            if is_command:
                if subparsers is None:
                    subparsers = parser.add_subparsers(dest="command")

                cls.extend_parser(
                    subparsers.add_parser(*arg.options, help=arg.description),
                    arg.arguments,
                )
            elif is_parameter:
                parser.add_argument(*arg.options, nargs=1)
            else:
                parser.add_argument(
                    *arg.options, action="count", default=SUPPRESS, help=arg.description
                )

        return parser, subparsers

    @property
    def parser(self) -> ConsoleArgumentParser:
        """Built-in Argument parser getter."""
        if self._parser is None:
            self._parser = ConsoleArgumentParser(
                prog=sys.argv[0],
                description=self.description,
                epilog=self.epilog,
                add_help=False,
            )

            self._parser, _ = self.extend_parser(
                parser=self._parser, args=self.arguments
            )

        return self._parser

    def parse(self, argv: t.List[str]) -> t.Tuple[t.Dict[str, str], t.List[str]]:
        """Return parsing result."""
        args, undef = self.parser.parse_known_args(argv)

        return vars(args), undef

    def help(self) -> str:
        """Print a help message, including the program usage and registered arguments."""
        output = io.StringIO()
        self.parser.print_help(file=output)
        return output.getvalue()
