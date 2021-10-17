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
from typing import Any
from typing import List


class BaseArgument(metaclass=abc.ABCMeta):
    """Argument Abstraction."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Class constructor."""
        self._options = [*args]
        self._description = ""
        self.__construct(**kwargs)

    def __construct(self, description: str = "") -> None:
        """Class strict constructor."""
        self._description = description

    @property
    def options(self) -> List[str]:
        """Options names getter."""
        return self._options

    @options.setter
    def options(self, options: List[str]) -> None:  # pragma: no cover
        """Options names setter."""
        # TODO: Add argument name validator IEEE Std 1003.1-2017
        self._options = options

    @property
    def description(self) -> str:
        """Argument description getter."""
        return self._description

    @description.setter
    def description(self, description: str) -> None:  # pragma: no cover
        """Argument description setter."""
        self._description = description
