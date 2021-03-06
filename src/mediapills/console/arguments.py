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
from typing import Any
from typing import List
from typing import Optional
from typing import Union

from mediapills.console.abc.arguments import BaseArgument
from mediapills.console.abc.arguments import TBaseArguments
from mediapills.console.abc.inputs import BaseInput
from mediapills.console.abc.outputs import BaseOutput

DefaultValue = Optional[Union[str, int, List[Union[str, int]]]]


"""A value must be passed when the option is used (e.g. --iterations=5 or -i5)."""
VALUE_REQUIRED = 1  # 2 ** 0

"""The option may or may not have a value (e.g. --yell or --yell=loud)."""
VALUE_OPTIONAL = 2  # 2 ** 1

"""The option accepts multiple values (e.g. --dir=/foo --dir=/bar)."""
VALUE_IS_ARRAY = 4  # 2 ** 2

ERR_MSG_INVALID_MODE = 'Argument mode "{mode}" is not valid.'

ERR_MSG_MODE_CONSTRAINT = (
    "Argument mode can not be VALUE_OPTIONAL and VALUE_REQUIRED simultaneously."
)

ERR_MSG_DEFAULT_ASSIGNMENT = (
    "Cannot set a default value except for VALUE_OPTIONAL mode."
)

ERR_MSG_DEFAULT_ARRAY_VALUE = "A default value for an array argument must be an list."

ERR_MSG_DEFAULT_VALUE_TYPE = "A default value should be 'int' or 'str' type."


class InputOption(BaseArgument):  # type: ignore
    """Input Argument Option implementation."""

    pass


class InputParameter(BaseArgument):  # type: ignore
    """Input Argument Parameter implementation."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Class constructor."""
        super().__init__(*args, description=kwargs.get("description", ""))
        self._mode = VALUE_OPTIONAL
        self._default: DefaultValue = None
        self.__construct(**kwargs)

    def __construct(
        self,
        mode: int = VALUE_OPTIONAL,
        default: DefaultValue = None,
        description: str = "",  # dead: disable
    ) -> None:
        """Class strict constructor."""
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

        if mode & VALUE_OPTIONAL and mode & VALUE_REQUIRED:
            raise ValueError(ERR_MSG_MODE_CONSTRAINT)

        self._mode = mode

    def is_optional(self) -> bool:  # dead: disable
        """Return True if an argument is VALUE_OPTIONAL."""
        return self._mode & VALUE_OPTIONAL > 0

    def is_required(self) -> bool:  # dead: disable
        """Return True if an argument is VALUE_REQUIRED."""
        return self._mode & VALUE_REQUIRED > 0

    def is_array(self) -> bool:
        """Return True if an argument is array type."""
        return self._mode & VALUE_IS_ARRAY > 0

    @property
    def default(self) -> DefaultValue:
        """Argument default value getter."""
        return self._default

    @default.setter
    def default(self, default: DefaultValue = None) -> None:
        """Argument default value setter."""
        if self.mode & VALUE_REQUIRED > 0 and default is not None:
            raise ValueError(ERR_MSG_DEFAULT_ASSIGNMENT)

        if self.is_array():
            if default is None:
                self._default = []
            elif not isinstance(default, list):
                raise ValueError(ERR_MSG_DEFAULT_ARRAY_VALUE)
        elif default is None:
            pass
        elif not isinstance(default, (str, int)) or isinstance(default, bool):
            raise ValueError(ERR_MSG_DEFAULT_VALUE_TYPE)

        self._default = default


TInputOptions = List[InputOption]
TInputParameters = List[InputParameter]


class InputCommand(BaseArgument):  # type: ignore
    """Interface for all console commands."""

    def __init__(
        self,
        *args: Any,
        arguments: Optional[TBaseArguments] = None,
        description: str = ""
    ) -> None:
        """Class constructor."""
        super().__init__(*args, description=description)
        self._arguments = arguments or []

    @property
    def arguments(self) -> TBaseArguments:
        """Command arguments getter."""
        return self._arguments

    def execute(self, stdin: BaseInput, stdout: BaseOutput) -> int:  # dead: disable
        """Execute the current command."""
        raise NotImplementedError()


TInputCommands = List[InputCommand]


# class CommandDispatcher(InputCommand):
#     """Decouple the implementation of a command from its commander."""
#
#     def register_handler(self, handler: InputCommand) -> None:
#         """Add the new handler to the list."""
#         pass
#
#     def remove_handler(self, name: str) -> None:
#         """Remove handler from the list."""
#         pass
#
#     @property
#     def commands(self) -> List[InputCommand]:
#         """Command sub-commands getter"""
#         return self._commands
#
#     def execute(self, stdin: BaseInput, stdout: BaseOutput) -> int:
#         """Execute the current command."""
#         raise NotImplementedError()
#
#     def has_command(self, name: str) -> bool:
#         """Return true if an command exists by name."""
#         raise NotImplementedError()
