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
import unittest
from typing import Any

from parameterized import parameterized

from mediapills.console.arguments.parameters import InputParameter


class TestInputParameter(unittest.TestCase):
    def test_default_should_be_valid(self) -> None:
        obj = InputParameter(name="test")

        self.assertEqual("test", obj.name)
        self.assertEqual("", obj.description)
        self.assertIsNone(obj.default)
        self.assertFalse(obj.is_array())
        self.assertTrue(obj.is_optional())
        self.assertFalse(obj.is_required())

    def test_required_should_be_required_only(self) -> None:
        obj = InputParameter(name="test", mode=InputParameter.VALUE_REQUIRED)

        self.assertFalse(obj.is_array())
        self.assertFalse(obj.is_optional())
        self.assertTrue(obj.is_required())

    def test_required_array_should_be_required_and_array(self) -> None:
        obj = InputParameter(
            name="test",
            mode=InputParameter.VALUE_REQUIRED | InputParameter.VALUE_IS_ARRAY,
        )

        self.assertTrue(obj.is_array())
        self.assertFalse(obj.is_optional())
        self.assertTrue(obj.is_required())

    def test_optional_should_be_optional_only(self) -> None:
        obj = InputParameter(name="test", mode=InputParameter.VALUE_OPTIONAL)

        self.assertFalse(obj.is_array())
        self.assertTrue(obj.is_optional())
        self.assertFalse(obj.is_required())

    def test_optional_array_should_be_optional_and_array(self) -> None:
        obj = InputParameter(
            name="test",
            mode=InputParameter.VALUE_OPTIONAL | InputParameter.VALUE_IS_ARRAY,
        )

        self.assertTrue(obj.is_array())
        self.assertTrue(obj.is_optional())
        self.assertFalse(obj.is_required())

    def test_required_optional_should_raise_error(self) -> None:
        with self.assertRaises(expected_exception=ValueError):
            InputParameter(
                name="test",
                mode=InputParameter.VALUE_REQUIRED | InputParameter.VALUE_OPTIONAL,
            )

    def test_invalid_mode_should_raise_error(self) -> None:
        with self.assertRaises(expected_exception=ValueError):
            InputParameter(name="test", mode=2 ** 3)

    def test_required_default_not_none_should_raise_error(self) -> None:
        with self.assertRaises(expected_exception=ValueError):
            InputParameter(
                name="test", mode=InputParameter.VALUE_REQUIRED, default="value"
            )

    def test_array_default_should_be_valid(self) -> None:
        with self.assertRaises(expected_exception=ValueError):
            InputParameter(
                name="test", mode=InputParameter.VALUE_IS_ARRAY, default="value"
            )

    @parameterized.expand(  # type: ignore
        [
            [value]
            for value in [
                True,
                1.1,
                {"key": "val"},
                ["el1", "el2"],
                ("arg1", "arg2"),
                {"opt1", "opt2"},
            ]
        ]
    )
    def test_default_type_should_be_valid(self, default: Any) -> None:
        with self.assertRaises(expected_exception=ValueError):
            InputParameter(name="test", default=default)
