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

from mediapills.console.inputs import ArgumentParserAwareInput
from mediapills.console.inputs import BaseInput
from mediapills.console.outputs import BaseOutput
from mediapills.console.outputs import ConsoleOutput


class Application:  # dead: disable
    """Interface  for the container a collection of commands."""

    @abc.abstractmethod
    def run(  # dead: disable
        self,
        stdin: t.Optional[BaseInput],
        stdout: t.Optional[BaseOutput],
        stderr: t.Optional[BaseOutput],
        *args: t.List[t.Any],  # dead: disable
        **kwargs: t.Dict[str, t.Any]  # dead: disable
    ) -> None:
        """Run the current application."""
        if stdin is None:
            stdin = ArgumentParserAwareInput()

        if stdout is None:
            stdout = ConsoleOutput()

        if stderr is None:
            stderr = ConsoleOutput()

        raise NotImplementedError()
