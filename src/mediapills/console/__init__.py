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

from mediapills.console.abc.inputs import BaseInput
from mediapills.console.abc.outputs import BaseConsoleOutput
from mediapills.console.abc.outputs import FAILURE
from mediapills.console.abc.outputs import SUCCESS
from mediapills.console.applications import ApplicationWithArguments
from mediapills.console.arguments import InputOption
from mediapills.console.arguments import InputParameter
from mediapills.console.arguments import TInputCommands
from mediapills.console.arguments import TInputOptions
from mediapills.console.arguments import TInputParameters
from mediapills.console.exceptions import ConsoleUnrecognizedArgumentsException
from mediapills.console.inputs import ConsoleInput
from mediapills.console.parsers import InputArgumentsParser


__all__ = ["option", "parameter", "Application"]

TCallable = t.Callable[..., t.Any]


def option(*args: t.Any, **kwargs: t.Any) -> InputOption:
    """Object InputOption builder."""
    return InputOption(*args, **kwargs)


def parameter(*args: t.Any, **kwargs: t.Any) -> InputParameter:
    """Object InputParameter builder."""
    return InputParameter(*args, **kwargs)


class Application(ApplicationWithArguments):
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
        self._options: TInputOptions = self.default_options
        self._parameters: TInputParameters = []
        self._commands: TInputCommands = []
        self._parser: t.Optional[InputArgumentsParser] = None
        self._entrypoint: t.Optional[TCallable] = None

    @property
    def parser(self) -> InputArgumentsParser:
        """Application input parser."""
        if self._parser is None:
            self._parser = InputArgumentsParser(
                arguments=[*self.parameters, *self.options, *self.commands]
            )
        return self._parser

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
        elif self._show_help:
            self.show_help()
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
            raise RuntimeError("Entrypoint is not TCallable.")

    def show_help(self, code: int = SUCCESS) -> None:
        """Show application help"""
        self.stdout.write(self.parser.help())
        exit(code)

    def entrypoint(
        self, *args: t.List[t.Any], **kwargs: t.Dict[t.Any, t.Any]
    ) -> TCallable:
        """Allow you to configure a application that will run as an executable."""

        def append_args(
            options: t.Optional[TInputOptions] = None,
            parameters: t.Optional[TInputParameters] = None,
        ) -> None:
            if options is not None:
                for opt in options:
                    self.options.append(opt)

            if parameters is not None:
                for param in parameters:
                    self.parameters.append(param)

        def decorator(func: TCallable) -> TCallable:
            # TODO raise error if already defined
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
