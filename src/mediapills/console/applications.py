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
import os
import sys
import typing as t
from typing import Optional

from mediapills.console import arguments
from mediapills.console.abc.inputs import BaseInput
from mediapills.console.abc.outputs import BaseConsoleOutput
from mediapills.console.exceptions import ConsoleUnrecognizedArgumentsException
from mediapills.console.inputs import ConsoleInput
from mediapills.console.outputs import FAILURE
from mediapills.console.outputs import SUCCESS
from mediapills.console.parsers import InputArgumentsParser
from mediapills.console.version import version as setup_version

PACKAGE_NAME = "mediapills.core"

InputOptions = t.List[arguments.InputOption]
InputParameters = t.List[arguments.InputParameter]
Callable = t.Callable[..., t.Any]


def option(*args: t.Any, **kwargs: t.Any) -> arguments.InputOption:
    """Object InputOption builder."""
    return arguments.InputOption(*args, **kwargs)


def parameter(*args: t.Any, **kwargs: t.Any) -> arguments.InputParameter:
    """Object InputParameter builder."""
    return arguments.InputParameter(*args, **kwargs)


class BaseApplication(metaclass=abc.ABCMeta):
    """Interface  for the container a collection of commands."""

    def __init__(
        self,
        stdout: Optional[BaseConsoleOutput] = None,
        stderr: Optional[BaseConsoleOutput] = None,
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
    def stdout(self) -> BaseConsoleOutput:
        """Application output setter."""
        return self._stdout

    @stdout.setter
    def stdout(self, stdout: BaseConsoleOutput) -> None:
        """Application output getter."""
        self._stdout = stdout

    @property
    def stderr(self) -> BaseConsoleOutput:
        """Application standard errors output setter."""
        return self._stderr

    @stderr.setter
    def stderr(self, stderr: BaseConsoleOutput) -> None:
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
    def run(self) -> None:
        """Run the current application."""
        raise NotImplementedError()

    @property
    def default_options(self) -> InputOptions:
        """Verbosity options getter."""
        options = []

        if self._show_help:  # Add show help option
            options.append(
                option("-h", "--help", description="show this help message and exit.")
            )

        if self._show_version:  # Add show version option
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
    def default_options(self) -> InputOptions:
        """Verbosity options getter."""
        options = (
            (
                ("-q", "--quiet",),
                "don't show progress meter or error messages (silent or quiet mode).",
            ),
            (
                ("-v",),
                (
                    "increase the verbosity of messages: "
                    "1 for normal output, 2 for more verbose output and 3 for debug."
                ),
            ),
        )

        return super().default_options + [
            option(*args, description=desc) for args, desc in options
        ]

    def apply_options(self, stdin: BaseInput) -> None:
        """Set output verbosity level."""
        super().apply_options(stdin)

        if stdin.has_arg("quiet"):
            self.stdout.set_quiet()

        if not stdin.has_arg("v"):
            return
        elif stdin.get_arg("v") == 1:
            self.stdout.set_verbose()
        elif stdin.get_arg("v") == 2:
            self.stdout.set_very_verbose()
        else:
            self.stdout.set_debug()


class Application(VerboseAwareApplication):
    """Collection of commands container facade."""

    def __init__(
        self,
        stdout: t.Optional[BaseConsoleOutput],
        stderr: t.Optional[BaseConsoleOutput],
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
        self._options: InputOptions = self.default_options
        self._parameters: InputParameters = []
        self._entrypoint: t.Optional[Callable] = None

    @property
    def parser(self) -> InputArgumentsParser:
        """Application input parser."""
        if self._parser is None:
            self._parser = InputArgumentsParser(
                arguments=[*self.parameters, *self.options, *self.commands]
            )
        return self._parser

    @property
    def options(self) -> InputOptions:
        """Application options getter."""
        return self._options

    @property
    def parameters(self) -> InputParameters:
        """Application parameters getter"""
        return self._parameters

    @property
    def commands(self) -> t.List[arguments.InputCommand]:
        """Application commands getter"""
        return []

    def run(self) -> None:
        """Run the current application command."""
        stdin = ConsoleInput(parser=self.parser)

        try:
            stdin.validate()
        except ConsoleUnrecognizedArgumentsException:
            self.show_help(FAILURE)

        self.apply_options(stdin=stdin)

        if len(self.commands):
            self.do_dispatch(stdin=stdin)
        elif self._entrypoint is not None:
            self.do_entrypoint(stdin=stdin)
        else:
            pass  # Nothing to run

    def do_dispatch(self, stdin: BaseInput) -> None:
        """Dispatch commands."""
        raise NotImplementedError()

    def do_entrypoint(self, stdin: BaseInput) -> None:
        """Run entrypoint."""
        if callable(self._entrypoint):
            self._entrypoint(stdin=stdin, stdout=self.stdout)
        else:
            raise RuntimeError("Entrypoint is not callable.")

    def show_help(self, code: int = SUCCESS) -> None:
        """Show application help"""
        self.stdout.write(self.parser.help())
        exit(code)

    def show_version(self) -> None:
        """Show application version."""
        sys_version = ".".join(
            (
                str(sys.version_info.major),
                str(sys.version_info.minor),
                str(sys.version_info.micro),
            )
        )

        ver = " ".join(
            "{app}/{ver}".format(**{"app": app, "ver": release})
            for app, release in (
                (sys.argv[0], self.version),
                ("Python", sys_version),
                (os.uname().sysname, os.uname().release),
                (PACKAGE_NAME, setup_version),
            )
        )

        self.stdout.write(ver)
        exit(SUCCESS)

    def entrypoint(
        self, *args: t.List[t.Any], **kwargs: t.Dict[t.Any, t.Any]
    ) -> Callable:
        """Allow you to configure a application that will run as an executable."""
        # TODO raise error if already defined
        def append_args(
            options: t.Optional[InputOptions] = None,
            parameters: t.Optional[InputParameters] = None,
        ) -> None:
            if options is not None:
                for arg in options:
                    self.options.append(arg)

            if parameters is not None:
                for arg in parameters:
                    self.parameters.append(arg)

        def decorator(func: Callable) -> Callable:
            self._entrypoint = func
            return func

        if len(kwargs) > 0:
            append_args(**kwargs)  # type: ignore
        elif len(args) == 1:
            ep = args[0]
            if callable(ep):
                return decorator(ep)

        return decorator

    def command(self, name: str) -> None:  # dead: disable
        """Decorate a view function to register command in application."""
        # TODO: implement
        # TODO: reset stdin

        raise NotImplementedError()
