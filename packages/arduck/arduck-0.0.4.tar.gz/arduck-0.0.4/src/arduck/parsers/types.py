"""Contains argument types."""

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


from typing import Literal

from jinja2 import TemplateNotFound

from .. import tokenizer
from ..arduino.keyboard import LAYOUTS
from ..modules import template as template_
from ..tokenizer import RawKeystroke


def key(argument: str) -> list[RawKeystroke]:
    """A series of keystrokes."""

    special_characters_mapping: dict[str, str] = {
        '\\t': '\t',
        '\\n': '\n',
        '\\r': '\r',
        '\\f': '\f',
        '\\v': '\v'
    }

    # fix misinterpreted special characters.
    for character, replacement in special_characters_mapping.items():
        argument = argument.replace(character, replacement)

    return tokenizer.to_keystrokes(argument)


def delay(argument: str) -> int:
    """Delay in milliseconds, strictly greater than 0."""


    if (ms := int(argument)) <= 0:
        raise ValueError('delay must be greater than 0')

    return ms


def key_or_delay(argument: str) -> list[int | RawKeystroke]:
    """A series of keystrokes and delays."""

    if argument.isnumeric():
        return [delay(argument)]

    return key(argument)


def keyboard_layout(argument: str) -> str:
    """A supported keyboard layout."""

    try:
        _constant = LAYOUTS[argument]
    except KeyError as e:
        raise ValueError from e

    return argument


def template(argument: str) -> str:
    """A valid sketch template."""

    try:
     _template = template_.get(argument)
    except TemplateNotFound as e:
        raise ValueError from e

    return argument


def repeat_every(argument: Literal[False] | str) -> Literal[False] | int:
    """Optionally repeat the injection every n milliseconds."""

    if isinstance(argument, bool) and argument is False:
        return argument

    return int(argument)


def words_per_minute(argument: str) -> int:
    """The speed at which keystrokes are sent, in words per minute."""

    if (wpm := int(argument)) < 0:
        raise ValueError('wpm must be a positive number')

    return wpm
