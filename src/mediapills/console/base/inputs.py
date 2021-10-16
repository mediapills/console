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
from typing import Optional


class BaseInput(metaclass=abc.ABCMeta):
    """Interface for all console commands."""

    @property
    @abc.abstractmethod
    def command(self) -> Optional[str]:
        """Return the first argument from the raw parameters (not parsed)."""
        raise NotImplementedError()

    @abc.abstractmethod
    def get_arg(self, name: str) -> Optional[str]:
        """Return the argument value for a given argument name."""
        raise NotImplementedError()

    @abc.abstractmethod
    def has_arg(self, name: str) -> Optional[str]:
        """Return true if an InputParameter object exists by name or position."""
        raise NotImplementedError()

    @abc.abstractmethod
    def get_args(self) -> List[str]:
        """Return all the given arguments merged with the default values."""
        raise NotImplementedError()

    @abc.abstractmethod
    def bind(self) -> None:
        """Binds the current Input instance with the given arguments and options."""
        raise NotImplementedError()

    @abc.abstractmethod
    def validate(self) -> None:
        """Validate arguments."""
        raise NotImplementedError()


class BaseConsoleInput(BaseInput, metaclass=abc.ABCMeta):
    """Input is the base class for all concrete Input classes."""

    pass
