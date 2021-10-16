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
from argparse import ArgumentParser
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from mediapills.console.base.arguments import BaseArgument


class InputParser(metaclass=abc.ABCMeta):
    """Abstract class for input parser."""

    @abc.abstractmethod
    def parse(self) -> Tuple[Dict[str, str], List[str]]:
        """Return parsing result."""
        raise NotImplementedError

    @abc.abstractmethod
    def print(self) -> None:
        """Print a help message, including the program usage and registered arguments."""
        raise NotImplementedError


class InputArgumentsParser(InputParser):
    """CLI arguments parser."""

    def __init__(
        self, arguments: List[BaseArgument], description: Optional[str] = ""
    ) -> None:
        """Class constructor."""
        self._arguments = arguments
        self._description = description
        self._parser: Optional[ArgumentParser] = None

    @property
    def arguments(self) -> List[BaseArgument]:
        """Arguments getter."""
        return self._arguments

    def parser(self) -> ArgumentParser:  # dead: disable
        """Built-in Argument parser getter."""
        # iterate via arguments
        raise NotImplementedError()

    def parse(self) -> Tuple[Dict[str, str], List[str]]:  # dead: disable
        """Return parsing result."""
        return {}, []

    def print(self) -> None:  # dead: disable
        """Print a help message, including the program usage and registered arguments."""
        raise NotImplementedError
