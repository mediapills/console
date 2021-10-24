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

from mediapills.console import Application, option, parameter
from mediapills.console.outputs import ConsoleOutput
from mediapills.console.inputs import ConsoleInput

if __name__ == "__main__":
    app = Application(stdout=ConsoleOutput(), stderr=ConsoleOutput())

    @app.entrypoint(
        options=[  # type: ignore
            option("-a", description="Show A."),
            option("-b", description="Show B."),
        ],
        parameters=[parameter("--param")],  # type: ignore
    )
    def print_me(stdin: ConsoleInput, stdout: ConsoleOutput) -> None:  # dead: disable
        """CLI command with arguments print message in STDOUT depend on arguments."""
        if stdin.has_arg("param"):
            stdout.write(
                "Parameter '--param' has been used with value '{value}'.".format(
                    value=stdin.get_arg("param")
                )
            )

        if stdin.has_arg("a"):
            stdout.write("Argument '-a' has been used .")

        if stdin.has_arg("b"):
            stdout.write("Argument '-b' has been used .")

        stdout.writeln("Application message goes here ...")

    app.run()
