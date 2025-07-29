"""Contains a collection of useful parent argument parsers.

Parent parsers should not rely on any argument parsing method (e.g. parse_args())
to parse their parsing, but should implement custom actions.
"""

# Copyright (C) 2025  Stefano Cuizza

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.


from argparse import Action, ArgumentParser
from typing import override

from .. import log


class HandleVerbosityAction(Action):
    """Cumulative action that updates the application logging level
    based on the value of argument.
    """

    @override
    def __init__(self, option_strings, dest, nargs=0, **kwargs):
        super().__init__(option_strings, dest, nargs, **kwargs)

    @override
    def __call__(self, parser, namespace, values, option_string=None):
        current_value: int = getattr(namespace, self.dest, 0)
        setattr(namespace, self.dest, updated_value := current_value + 1)

        # the maximum value for verbosity is 5.
        if (verbosity := min(updated_value, 5)) > 0:
            log.set_root_logger_level(verbosity * 10)


class HandleQuietnessAction(Action):
    """Cumulative action that updates the application logging level
    based on the value of argument.
    """

    @override
    def __init__(self, option_strings, dest, nargs=0, **kwargs):
        super().__init__(option_strings, dest, nargs, **kwargs)

    @override
    def __call__(self, parser, namespace, values, option_string=None):
        current_value: int = getattr(namespace, self.dest, 0)
        setattr(namespace, self.dest, updated_value := current_value + 1)

        # the maximum value for quietness is 3.
        if (quietness := min(updated_value, 3)) > 0:
            log.set_root_logger_level((quietness + 2) * 10)


class VerboseArgumentParser(ArgumentParser):
    """Adds the ability to change verbosity through the CLI.

    New flags:
        -v, --verbose:
            set the verbosity level. This option is additive,
            and can be used up to 5 times.
        -q, --quiet:
            give less output. This option is additive,
            and can be used up to 3 times.
    """

    @override
    def __init__(self, *args, **kwargs):
        kwargs['add_help'] = False
        super().__init__(*args, **kwargs)

        self.add_argument(
            '-q', '--quiet',
            action=HandleQuietnessAction,
            default=0,
            dest='quiet',
            help=(
                'give less output. option is additive, and can '
                'be used up to 3 times (warning/error/critical)'
            ),
            required=False,
        )

        self.add_argument(
            '-v', '--verbose',
            action=HandleVerbosityAction,
            default=0,
            dest='verbosity',
            help=(
                'set the verbosity level. option is additive, '
                'and can be used up to 5 times '
                '(debug/info/warning/error/critical). '
                '(default: info)'
            ),
            required=False,
        )
