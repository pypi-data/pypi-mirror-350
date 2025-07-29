"""Special module that runs when the package is invoked directly
 from the command line using the -m flag.

For more information, see:
https://docs.python.org/3/library/__main__#main-py-in-python-packages.

All CLI entry points should be initialized in this module.
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


from argparse import ArgumentParser, Namespace
import logging
from typing import Type

from . import cli
from .modules import log
from .parsers import MainArgumentParser


logger = logging.getLogger(__name__)


def init_cli_with_argument_parser(argument_parser: Type[ArgumentParser]) -> Namespace:
    """Initializes everything that is required by a Command Line Interface.

    The ArgumentParser class will be used to parse the command line parsing.

    Args:
        argument_parser:
            an **uninitialized** ArgumentParser class.

    Returns:
        the parsed command line parsing as a Namespace object.
    """

    log.init()

    with log.deferred_logging():
        log.set_root_logger_level(logging.INFO)

        # calling the ArgumentParser under deferred_logging is necessary to make
        # sure that the cached log records are handled with the correct logging
        # level.
        return argument_parser().parse_args()


def main() -> None:
    """Main CLI entry point."""

    arguments: Namespace = init_cli_with_argument_parser(MainArgumentParser)
    cli.main(arguments)


if __name__ == '__main__':
    main()
