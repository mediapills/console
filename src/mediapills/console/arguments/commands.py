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
from typing import List

from mediapills.console import arguments
from mediapills.console.arguments.options import InputOption
from mediapills.console.arguments.parameters import InputParameter
from mediapills.console.inputs import BaseInput
from mediapills.console.outputs import BaseOutput


class InputCommand(arguments.BaseArgument):
    """Interface for all console commands."""

    # More info: https://tldp.org/LDP/abs/html/exitcodes.html
    """No error. The script executed successfully."""
    SUCCESS = 0  # dead: disable

    """Catchall for general errors."""
    FAILURE = 1  # dead: disable

    """Misuse of shell builtins (according to Bash documentation)."""
    INVALID = 2  # dead: disable

    def __init__(self, name: str, description: str = ""):
        """Class constructor."""
        super().__init__(name=name, description=description)
        self._commands = []  # type: List[InputCommand]
        self._options = []  # type: List[InputOption]
        self._parameters = []  # type: List[InputParameter]

    @property
    def commands(self) -> List["InputCommand"]:  # dead: disable
        """Command sub-commands getter"""
        return self._commands

    @property
    def options(self) -> List[InputOption]:  # dead: disable
        """Command options getter"""
        return self._options

    @property
    def parameters(self) -> List[InputParameter]:  # dead: disable
        """Command parameters getter"""
        return self._parameters

    @abc.abstractmethod
    def execute(self, stdin: BaseInput, stdout: BaseOutput) -> int:  # dead: disable
        """Execute the current command."""
        raise NotImplementedError()
