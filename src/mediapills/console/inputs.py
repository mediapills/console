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


class BaseInput(metaclass=abc.ABCMeta):
    """Interface for all console commands."""

    @property
    @abc.abstractmethod
    def first(self) -> t.Optional[str]:  # dead: disable
        """Return the first argument from the raw parameters (not parsed)."""
        raise NotImplementedError()

    @abc.abstractmethod
    def get_args(self) -> t.Optional[t.List[str]]:  # dead: disable
        """Return all the given arguments merged with the default values."""
        raise NotImplementedError()

    @abc.abstractmethod
    def get_arg(self, name: str) -> t.Optional[str]:  # dead: disable
        """Return the argument value for a given argument name."""
        raise NotImplementedError()

    @abc.abstractmethod
    def has_arg(self, name: str) -> t.Optional[str]:  # dead: disable
        """Return true if an InputArgument object exists by name or position."""
        raise NotImplementedError()


class Input(BaseInput, metaclass=abc.ABCMeta):
    """Input is the base class for all concrete Input classes."""

    pass


class ArgumentParserAwareInput(Input):
    """Command argument parser based on argparse."""

    def __init__(self, description: str = ""):
        """Class constructor."""
        self._description = description

    @property
    def first(self) -> t.Optional[str]:  # dead: disable
        """Return the first argument from the raw parameters (not parsed)."""
        # TODO: implement this method
        raise NotImplementedError()

    def get_args(self) -> t.Optional[t.List[str]]:  # dead: disable
        """Return all the given arguments merged with the default values."""
        # TODO: implement this method
        raise NotImplementedError()

    def get_arg(self, name: str) -> t.Optional[str]:  # dead: disable
        """Return the argument value for a given argument name."""
        # TODO: implement this method
        raise NotImplementedError()

    def has_arg(self, name: str) -> t.Optional[str]:  # dead: disable
        """Return true if an InputArgument object exists by name or position."""
        # TODO: implement this method
        raise NotImplementedError()
