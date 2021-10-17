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

from mediapills.console.abc.outputs import BaseOutput
from mediapills.console.arguments import InputCommand
from mediapills.console.arguments import InputOption
from mediapills.console.arguments import InputParameter
from mediapills.console.exceptions import ConsoleUnrecognizedArgumentsException
from mediapills.console.inputs import ConsoleInput
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
    ):
        """Class constructor."""
        self._stdout = stdout
        self._stderr = stderr
        self._description = description
        self._version = version

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
    def run(self) -> None:
        """Run the current application."""
        raise NotImplementedError()


class Application(BaseApplication):  # dead: disable
    """Collection of commands container facade."""

    __slots__ = ["_entrypoint"]

    def __init__(
        self,
        stdout: t.Optional[BaseOutput],
        stderr: t.Optional[BaseOutput],
        description: str = "",
        version: str = "",
    ):
        """Class constructor."""
        super().__init__(
            stdout=stdout, stderr=stderr, description=description, version=version,
        )
        self._parser: t.Optional[InputArgumentsParser] = None
        """
        Verbosity levels:
        -v: Show informational messages that highlight the progress of the application at
        coarse-grained level.
        -vv: Show fine-grained informational events that are most useful to debug an
        application.
        -vvv: Show finer-grained informational events that include tracing.
        """
        self._options: t.List[InputOption] = []
        self.__build_default_options()

    def __build_default_options(self) -> None:
        self._options.append(
            option("-V", "--version", description="Show version number and quit.")
        )
        q_desc = "Silent or quiet mode. Don't show progress meter or error messages."
        self._options.append(option("-q", "--quiet", description=q_desc,))
        v_desc = "Verbosity level can be controlled globally for all commands."
        self._options.append(
            # parser.add_argument('--verbose', '-v', action='count', default=0)
            option("-vvv", description=v_desc,)
        )

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
            self.stdout.write(self.parser.help())

        raise NotImplementedError

    def show_version(self) -> None:  # dead: disable
        """Show application version."""
        # {prog}/{version} Python/{python version} {OS}/{OS version}
        # {mediapills.console}/{version}
        # return self._version
        pass

    def command(self, name: str) -> None:
        """Decorate a view function to register command in application."""
        # TODO: implement
        # TODO: reset stdin
        raise NotImplementedError()
