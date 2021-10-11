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

from mediapills.console.arguments import BaseArgument


class BaseArgumentsParser(  # dead: disable
    list, metaclass=abc.ABCMeta  # type: ignore
):
    """Abstract class for input parser."""

    def append(self, __object: BaseArgument) -> None:
        """Append object to the end of the list."""
        return list.append(self, __object)

    def insert(self, __index: int, __object: BaseArgument) -> None:
        """Insert object before index."""
        return list.insert(self, __index, __object)

    def __add__(self, x: List[BaseArgument]) -> List[BaseArgument]:
        """Return self+value."""
        return list.__add__(self, x)

    # TODO: add more magic methods
