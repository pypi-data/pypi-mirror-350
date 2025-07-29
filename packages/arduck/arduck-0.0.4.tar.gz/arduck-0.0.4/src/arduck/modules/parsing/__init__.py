"""Argument parsing module.

Contains extendable ArgumentParser subclasses, formatters and helper functions.
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


from abc import ABC, abstractmethod
from argparse import (
    ArgumentParser,
    HelpFormatter,
    Namespace,
)
from collections.abc import Sequence
import logging
from typing import Optional, override


logger = logging.getLogger(__name__)


# ruamel (2020, March 30). Argparse improvements. SourceForge.
# https://sourceforge.net/projects/ruamel-std-argparse/.
class SmartFormatter(HelpFormatter):
    """Enables RawTextHelpFormatter for help messages that begin with `R|`
    and preserves line breaks in the `version` action.
    """

    def _fill_text(self, text, width, indent):
        return ''.join([indent + line for line in text.splitlines(True)])

    def _split_lines(self, text, width):
        if text.startswith('R|'):
            return text[2:].splitlines()

        return HelpFormatter._split_lines(self, text, width)


class ExtendableArgumentParser(ABC, ArgumentParser):
    """Argument parser with extendable functionality.

    Implement two private methods to extend functionality:
     - `_extend_arguments()` to add new arguments.
     - `_extend_subparsers()` to add new subparsers.
    """

    @override
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self._subparsers = None
        self._parents: list[ArgumentParser] = kwargs.get('parents', [])

        self._extend_arguments()
        self._extend_subparsers()

    @abstractmethod
    def _extend_arguments(self) -> None:
        """Adds new arguments."""

    @abstractmethod
    def _extend_subparsers(self) -> None:
        """Adds new subparsers."""

    @override
    def parse_args(
            self,
            args: Optional[Sequence[str]] = None,
            namespace: Optional[Namespace] = None,
    ) -> Namespace:
        namespace = super().parse_args(args=args, namespace=namespace)

        logger.debug('parsing: %r.', vars(namespace))
        return namespace

    @property
    def subparsers(self):
        """The argument parser subparsers.

        Subparsers are loaded lazily to avoid unnecessary overhead.
        """

        if not self._subparsers:
            # enable subparsers only if needed, to avoid weird artifacts in the help message.
            self._subparsers = self.add_subparsers(parser_class=ArgumentParser, dest='subparser')

        return self._subparsers
