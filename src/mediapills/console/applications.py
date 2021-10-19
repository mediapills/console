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
from typing import Optional

from mediapills.console.abc.inputs import BaseInput
from mediapills.console.abc.outputs import BaseConsoleOutput
from mediapills.console.abc.outputs import SUCCESS
from mediapills.console.arguments import InputOption
from mediapills.console.arguments import TInputCommands
from mediapills.console.arguments import TInputOptions
from mediapills.console.arguments import TInputParameters


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
    def default_options(self) -> TInputOptions:
        """Verbosity options getter."""
        options = []

        if self._show_help:  # Add show help option
            options.append(
                InputOption(
                    "-h", "--help", description="show this help message and exit."
                )
            )

        if self._show_version:  # Add show version option
            options.append(
                InputOption(
                    "-V", "--version", description="show version number and quit."
                )
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
            )
        )

        self.stdout.write(ver)
        exit(SUCCESS)


class VerboseAwareApplication(BaseApplication, metaclass=abc.ABCMeta):
    """Verbose aware application.
    Verbosity levels:
        -v: Show informational messages that highlight the progress of the application at
        coarse-grained level.
        -vv: Show fine-grained informational events that are most useful to debug an
        application.
        -vvv: Show finer-grained informational events that include tracing.
    """

    @property
    def default_options(self) -> TInputOptions:
        """Verbosity options getter."""
        options = super().default_options

        options.append(
            InputOption(
                "-q",
                "--quiet",
                description=(
                    "don't show progress meter or error messages (silent or quiet mode)."
                ),
            )
        )

        options.append(
            InputOption(
                "-v",
                description=(
                    "increase the verbosity of messages: "
                    "1 for normal output, 2 for more verbose output and more for debug."
                ),
            )
        )

        return options

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


class ApplicationWithArguments(VerboseAwareApplication, metaclass=abc.ABCMeta):
    """Abstract Base Application with arguments."""

    def __init__(
        self,
        stdout: Optional[BaseConsoleOutput],
        stderr: Optional[BaseConsoleOutput],
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
        self._options: TInputOptions = self.default_options
        self._parameters: TInputParameters = []
        self._commands: TInputCommands = []

    @property
    def options(self) -> TInputOptions:
        """Application options getter."""
        return self._options

    @property
    def parameters(self) -> TInputParameters:
        """Application parameters getter"""
        return self._parameters

    @property
    def commands(self) -> TInputCommands:
        """Application commands getter"""
        return self._commands
