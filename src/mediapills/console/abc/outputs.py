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

VERBOSITY_QUIET = 2 ** 3
VERBOSITY_NORMAL = 2 ** 4
VERBOSITY_VERBOSE = 2 ** 5
VERBOSITY_VERY_VERBOSE = 2 ** 6
VERBOSITY_DEBUG = 2 ** 7

OUTPUT_NORMAL = 2 ** 0  # dead: disable
OUTPUT_RAW = 2 ** 1  # dead: disable
OUTPUT_PLAIN = 2 ** 2  # dead: disable

# More info: https://tldp.org/LDP/abs/html/exitcodes.html
"""No error. The script executed successfully."""
SUCCESS = 0

"""Catchall for general errors."""
FAILURE = 1

"""Misuse of shell builtins (according to Bash documentation)."""
INVALID = 2  # dead: disable


class BaseOutput(metaclass=abc.ABCMeta):
    """Abstract Base Class for all Output classes."""

    @abc.abstractmethod
    def write(self, msg: str, newline: bool = False, options: int = 0) -> None:
        """Write a message to the output."""
        raise NotImplementedError()

    @abc.abstractmethod
    def writeln(self, msg: str, options: int = 0) -> None:
        """Write a message to the output and adds a newline at the end."""
        raise NotImplementedError()


class BaseVerboseAwareOutput(BaseOutput, metaclass=abc.ABCMeta):
    """Verbose aware base output."""

    def __init__(self, verbosity: int = VERBOSITY_NORMAL):
        """Class constructor."""
        self._verbosity = verbosity

    @property
    def verbosity(self) -> int:
        """Verbosity of the output getter."""
        return self._verbosity

    @verbosity.setter
    def verbosity(self, verbosity: int) -> None:
        """Verbosity of the output setter."""
        self._verbosity = verbosity

    def set_quiet(self) -> None:
        """Set level of verbosity status tp quiet."""
        self.verbosity = self.verbosity | VERBOSITY_QUIET

    def set_verbose(self) -> None:
        """Set status of verbosity level to verbose."""
        self.verbosity = self.verbosity | VERBOSITY_VERBOSE

    def set_very_verbose(self) -> None:
        """Set level of verbosity status to very verbose."""
        self.verbosity = self.verbosity | VERBOSITY_VERY_VERBOSE

    def set_debug(self) -> None:
        """Set level of verbosity status to debug."""
        self.verbosity = self.verbosity | VERBOSITY_DEBUG

    # @property
    # def quiet(self) -> bool:
    #     """Level of verbosity status is quiet (-q)."""
    #     return self.verbosity & VERBOSITY_QUIET > 0
    #
    # @property
    # def verbose(self) -> bool:
    #     """Status of verbosity level is verbose (-v)."""
    #     return self.verbosity & VERBOSITY_VERBOSE > 0
    #
    # @property
    # def very_verbose(self) -> bool:
    #     """Level of verbosity status is very verbose (-vv)."""
    #     return self.verbosity & VERBOSITY_VERY_VERBOSE > 0
    #
    # @property
    # def debug(self) -> bool:
    #     """Level of verbosity status is debug (-vvv)."""
    #     return self.verbosity & VERBOSITY_DEBUG > 0


class BaseConsoleOutput(BaseVerboseAwareOutput, metaclass=abc.ABCMeta):
    """Abstract Base Class for all Console Output classes."""

    pass
