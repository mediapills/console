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
from typing import Optional

from mediapills.console.base.outputs import BaseOutput


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
