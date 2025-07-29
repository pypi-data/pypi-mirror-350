"""Contains logging helper functions and custom handlers/formatters."""

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


from collections import deque
from collections.abc import Callable
from contextlib import contextmanager
import logging
from sys import stdout
from typing import override

from .ansi import Fore, Style


class LoggingFormatter(logging.Formatter):
    """Base logging formatter that supports colorful output.

    Attributes:
        record_format_strings:
          dict mapping logging levels to their corresponding format strings.
    """

    record_format_strings: dict[int, str] = {
        logging.NOTSET:
            '%(message)s',

        logging.DEBUG:
            '[DEBUG] %(name)s:%(lineno)s %(message)s',

        logging.INFO:
            f'{Fore.LIGHTWHITE_EX}'
            f'[INFO] %(message)s'
            f'{Fore.RESET}',

        logging.WARNING:
            f'{Fore.YELLOW}'
            f'[WARNING] %(message)s'
            f'{Fore.RESET}',

        logging.ERROR:
            f'{Fore.LIGHTRED_EX}'
            f'[{Style.ITALIC}ERROR{Style.RESET_ITALIC}] '
            f'%(message)s'
            f'{Fore.RESET}',

        logging.CRITICAL:
            f'{Fore.LIGHTMAGENTA_EX}'
            f'[{Style.ITALIC}CRITICAL{Style.RESET_ITALIC}] '
            f'{Style.UNDERLINE}%(message)s{Style.RESET_UNDERLINE}'
            f'{Fore.RESET}',
    }

    @override
    def format(self, record: logging.LogRecord) -> str:
        """Formats the log record as text.

        Args:
            record:
                logging record to format.
        """

        fmt = self.record_format_strings.get(
            record.levelno,
            '%(message)s',
        )

        return logging.Formatter(fmt).format(record)


def init() -> None:
    """Initializes the package logger."""

    root = logging.getLogger()

    console_stream_handler = logging.StreamHandler(
        stream=stdout,
    )
    console_stream_handler.setLevel(logging.NOTSET)
    console_stream_handler.setFormatter(LoggingFormatter())

    root.addHandler(console_stream_handler)
    root.setLevel(logging.NOTSET)


def set_root_logger_level(level: int | str) -> None:
    """Changes the root logger logging level.

    Args:
        level:
            a valid logging level.
    """

    logging.getLogger().setLevel(level)
    for handler in logging.getLogger().handlers:
        handler.setLevel(level)


@contextmanager
def apply_filter(logging_filter: Callable[[logging.LogRecord], bool]):
    """Context manager that applies a filter to the root logger.

    Args:
        logging_filter:
            a logging filter (https://docs.python.org/3/library/logging.html#filter-objects).

    """

    logging.getLogger().addFilter(logging_filter)
    for handler in logging.getLogger().handlers:
        handler.addFilter(logging_filter)

    try:
        yield None
    finally:
        logging.getLogger().removeFilter(logging_filter)
        for handler in logging.getLogger().handlers:
            handler.removeFilter(logging_filter)


@contextmanager
def deferred_logging():
    """Context manager that caches logging calls and handles them all on exit."""

    cached_records = deque()

    def cache_filter(record: logging.LogRecord) -> bool:
        """"""

        cached_records.append(record)
        return False

    try:
        with apply_filter(cache_filter):
            yield None
    finally:
        for record in cached_records:
            logging.getLogger().handle(record)
