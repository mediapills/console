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

REQUIRED = 2 ** 0
OPTIONAL = 2 ** 1
IS_ARRAY = 2 ** 2

ERR_MSG_INVALID_MODE = 'Argument mode "{mode}" is not valid.'
ERR_MSG_MODE_CONSTRAINT = (
    "Argument mode can not be OPTIONAL and REQUIRED simultaneously."
)
ERR_MSG_DEFAULT_ASSIGNMENT = "Cannot set a default value except for OPTIONAL mode."
ERR_MSG_DEFAULT_ARRAY_VALUE = "A default value for an array argument must be an list."
ERR_MSG_DEFAULT_VALUE_TYPE = "A default value should be 'int' or 'str' type."

TYPE_DEFAULT = t.Optional[t.Union[str, int, t.List[t.Union[str, int]]]]


class BaseArgument(metaclass=abc.ABCMeta):
    """Argument Abstract class."""

    def __init__(self, name: str, description: str = ""):
        """Class constructor."""
        self._name = name
        self._description = description

    @property
    def name(self) -> str:
        """Argument name getter."""
        return self._name

    @name.setter
    def name(self, name: str) -> None:  # pragma: no cover
        """Argument name setter."""
        # TODO: Add argument name validator IEEE Std 1003.1-2017
        self._name = name

    @property
    def description(self) -> str:
        """Argument description getter."""
        return self._description

    @description.setter
    def description(self, description: str) -> None:  # pragma: no cover
        """Argument description setter."""
        self._description = description


class InputArgument(BaseArgument):  # dead: disable
    """Input Argument implementation."""

    def __init__(
        self,
        name: str,
        mode: int = OPTIONAL,
        description: str = "",
        default: t.Optional[t.Any] = None,
    ):
        """Class constructor."""
        super().__init__(name=name, description=description)
        self._mode = OPTIONAL
        self._default = None
        self.mode = mode
        self.default = default

    @property
    def mode(self) -> int:
        """Argument mode getter."""
        return self._mode

    @mode.setter
    def mode(self, mode: int) -> None:
        """Argument mode setter."""
        if mode > 7 or mode < 1:
            raise ValueError(ERR_MSG_INVALID_MODE.format(mode=mode))

        if mode & OPTIONAL and mode & REQUIRED:
            raise ValueError(ERR_MSG_MODE_CONSTRAINT)

        self._mode = mode

    def is_optional(self) -> bool:  # dead: disable
        """Return True if an argument is optional."""
        return self._mode & OPTIONAL > 0

    def is_required(self) -> bool:  # dead: disable
        """Return True if an argument is required."""
        return self._mode & REQUIRED > 0

    def is_array(self) -> bool:
        """Return True if an argument is array type."""
        return self._mode & IS_ARRAY > 0

    @property
    def default(self) -> TYPE_DEFAULT:
        """Argument default value getter."""
        return self._default

    @default.setter
    def default(self, default: TYPE_DEFAULT = None) -> None:
        """Argument default value setter."""
        if self.mode & REQUIRED > 0 and default is not None:
            raise ValueError(ERR_MSG_DEFAULT_ASSIGNMENT)

        if self.is_array():
            if default is None:
                self._default = []
            elif not isinstance(default, list):
                raise ValueError(ERR_MSG_DEFAULT_ARRAY_VALUE)
        elif default is None:
            pass
        elif not isinstance(default, (str, int)) or isinstance(default, (bool)):
            raise ValueError(ERR_MSG_DEFAULT_VALUE_TYPE)

        self._default = default
