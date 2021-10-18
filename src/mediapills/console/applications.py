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
from typing import Optional

from mediapills.console.abc import outputs
from mediapills.console.abc.inputs import BaseInput
from mediapills.console.abc.outputs import BaseOutput
from mediapills.console.arguments import InputCommand
from mediapills.console.arguments import InputOption
from mediapills.console.arguments import InputParameter
from mediapills.console.exceptions import ConsoleUnrecognizedArgumentsException
from mediapills.console.inputs import ConsoleInput
from mediapills.console.outputs import FAILURE
from mediapills.console.outputs import SUCCESS
from mediapills.console.parsers import InputArgumentsParser


def option(*args: t.Any, **kwargs: t.Any) -> InputOption:
    """Object InputOption builder."""
    return InputOption(*args, **kwargs)


def parameter(*args: t.Any, **kwargs: t.Any) -> InputParameter:  # dead: disable
    """Object InputParameter builder."""
    return InputParameter(*args, **kwargs)


class BaseApplication(metaclass=abc.ABCMeta):
    """Interface  for the container a collection of commands."""

    def __init__(
        self,
        stdout: Optional[BaseOutput] = None,
        stderr: Optional[BaseOutput] = None,
        description: str = "",
        version: str = "",
        show_help: bool = False,
        show_version: bool = False,
    ):
        """Class constructor."""
        self._stdout = stdout
        self._stderr = stderr
        self._description = description
        self._version = version
        self._show_help = show_help
        self._show_version = show_version

    @property
    def stdout(self) -> BaseOutput:
        """Application output setter."""
        return self._stdout

    @stdout.setter
    def stdout(self, stdout: BaseOutput) -> None:
        """Application output getter."""
        self._stdout = stdout

    @property
    def stderr(self) -> BaseOutput:
        """Application standard errors output setter."""
        return self._stderr

    @stderr.setter
    def stderr(self, stderr: BaseOutput) -> None:
        """Application standard errors output getter."""
        self._stderr = stderr

    @property
    def description(self) -> str:
        """Application description getter."""
        return self._description

    @description.setter
    def description(self, description: str) -> None:
        """Application description setter."""
        self._description = description

    @property
    def version(self) -> str:
        """Application description getter."""
        return self._version

    @version.setter
    def version(self, version: str) -> None:
        """Application description setter."""
        self._version = version

    @abc.abstractmethod
    def run(self) -> None:  # dead: disable
        """Run the current application."""
        raise NotImplementedError()

    @property
    def default_options(self) -> t.List[InputOption]:
        """Verbosity options getter."""
        options = []

        if self._show_help:  # Add version message
            options.append(
                option("-h", "--help", description="show this help message and exit.")
            )

        if self._show_version:  # Add help message
            options.append(
                option("-V", "--version", description="show version number and quit.")
            )

        return options

    def apply_options(self, stdin: BaseInput) -> None:
        """Set default options."""
        if stdin.has_arg("help"):
            self.show_help()

        if stdin.has_arg("version"):
            self.show_version()

    @abc.abstractmethod
    def show_help(self) -> None:
        """Show application version."""
        raise NotImplementedError()

    @abc.abstractmethod
    def show_version(self) -> None:
        """Show application version."""
        raise NotImplementedError()


class VerboseAwareApplication(BaseApplication, metaclass=abc.ABCMeta):
    """Verbose aware application.
    Verbosity levels:
            -v: Show informational messages that highlight the progress of the
            application at coarse-grained level.
            -vv: Show fine-grained informational events that are most useful to debug an
            application.
            -vvv: Show finer-grained informational events that include tracing.
    """

    @property
    def default_options(self) -> t.List[InputOption]:
        """Verbosity options getter."""
        options = (
            (
                ("-q", "--quiet",),
                "don't show progress meter or error messages (silent or quiet mode).",
            ),
            (("-v",), "set output verbosity level from verbose (-v) to debug (-vvv).",),
        )

        return super().default_options + [
            option(*args, description=desc) for args, desc in options
        ]

    def apply_options(self, stdin: BaseInput) -> None:
        """Set output verbosity level."""
        super().apply_options(stdin)

        if stdin.has_arg("quiet"):
            self.stdout.verbosity = self.stdout.verbosity | outputs.VERBOSITY_QUIET

        verbose = stdin.get_arg("v")
        if verbose:
            if verbose == 1:
                self.stdout.verbosity = (
                    self.stdout.verbosity | outputs.VERBOSITY_VERBOSE
                )
            elif verbose == 2:
                self.stdout.verbosity = (
                    self.stdout.verbosity | outputs.VERBOSITY_VERY_VERBOSE
                )
            elif verbose == 3:
                self.stdout.verbosity = self.stdout.verbosity | outputs.VERBOSITY_DEBUG


class Application(VerboseAwareApplication):  # dead: disable
    """Collection of commands container facade."""

    def __init__(
        self,
        stdout: t.Optional[BaseOutput],
        stderr: t.Optional[BaseOutput],
        description: str = "",
        version: str = "",
        show_help: bool = False,
        show_version: bool = False,
    ):
        """Class constructor."""
        super().__init__(
            stdout=stdout,
            stderr=stderr,
            description=description,
            version=version,
            show_version=show_version,
            show_help=show_help,
        )
        self._parser: t.Optional[InputArgumentsParser] = None
        self._options: t.List[InputOption] = self.default_options

    @property
    def parser(self) -> InputArgumentsParser:
        """Application input parser."""
        if self._parser is None:
            self._parser = InputArgumentsParser(
                arguments=[*self.parameters, *self.options, *self.commands]
            )
        return self._parser

    @property
    def options(self) -> t.List[InputOption]:
        """Application options getter."""
        return self._options

    @property
    def parameters(self) -> t.List[InputParameter]:
        """Application parameters getter"""
        return []

    @property
    def commands(self) -> t.List[InputCommand]:
        """Application commands getter"""
        return []

    def run(self) -> None:  # dead: disable
        """Run the current application command."""
        stdin = ConsoleInput(parser=self.parser)

        try:
            stdin.validate()
        except ConsoleUnrecognizedArgumentsException:
            self.show_help(FAILURE)

        self.apply_options(stdin=stdin)

    def show_help(self, code: int = SUCCESS) -> None:
        """Show application help"""
        self.stdout.write(self.parser.help())
        exit(code)

    def show_version(self) -> None:
        """Show application version."""
        # {prog}/{version} Python/{python version} {OS}/{OS version}
        # {mediapills.console}/{version}
        self.stdout.write(self.version)
        exit(SUCCESS)

    def command(self, name: str) -> None:  # dead: disable
        """Decorate a view function to register command in application."""
        # TODO: implement
        # TODO: reset stdin

        raise NotImplementedError()
