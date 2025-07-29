"""This module extends colorama's ANSI codes.

All AnsiType classes store only the ANSI integer codes, while Fore, Back, and Style store the formatted ANSI codes.

Typical usage example:

    print(f'{Fore.RED}helloworld!{Fore.RESET}')
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


from typing import Final

from colorama.ansi import AnsiCodes


class AnsiFore(AnsiCodes):
    """Struct containing ANSI foreground int codes."""

    BLACK: Final[int] = 30
    RED: Final[int] = 31
    GREEN: Final[int] = 32
    YELLOW: Final[int] = 33
    BLUE: Final[int] = 34
    MAGENTA: Final[int] = 35
    CYAN: Final[int] = 36
    WHITE: Final[int] = 37

    LIGHTBLACK_EX: Final[int] = 90
    LIGHTRED_EX: Final[int] = 91
    LIGHTGREEN_EX: Final[int] = 92
    LIGHTYELLOW_EX: Final[int] = 93
    LIGHTBLUE_EX: Final[int] = 94
    LIGHTMAGENTA_EX: Final[int] = 95
    LIGHTCYAN_EX: Final[int] = 96
    LIGHTWHITE_EX: Final[int] = 97

    RESET: Final[int] = 39


class AnsiBack(AnsiCodes):
    """Struct containing ANSI background int codes."""

    BLACK: Final[int] = 40
    RED: Final[int] = 41
    GREEN: Final[int] = 42
    YELLOW: Final[int] = 43
    BLUE: Final[int] = 44
    MAGENTA: Final[int] = 45
    CYAN: Final[int] = 46
    WHITE: Final[int] = 47

    LIGHTBLACK_EX: Final[int] = 100
    LIGHTRED_EX: Final[int] = 101
    LIGHTGREEN_EX: Final[int] = 102
    LIGHTYELLOW_EX: Final[int] = 103
    LIGHTBLUE_EX: Final[int] = 104
    LIGHTMAGENTA_EX: Final[int] = 105
    LIGHTCYAN_EX: Final[int] = 106
    LIGHTWHITE_EX: Final[int] = 107

    RESET: Final[int] = 49


class AnsiStyle(AnsiCodes):
    """Struct containing ANSI style int codes."""

    BRIGHT: Final[int] = 1
    DIM: Final[int] = 2
    ITALIC: Final[int] = 3
    UNDERLINE: Final[int] = 4
    BLINKINGMODE: Final[int] = 5
    NEGATIVE: Final[int] = 7
    HIDDEN: Final[int] = 8
    STRIKETHROUGH: Final[int] = 9

    RESET_BRIGHT: Final[int] = 22
    RESET_DIM: Final[int] = 22
    RESET_ITALIC: Final[int] = 23
    RESET_UNDERLINE: Final[int] = 24
    RESET_BLINKINGMODE: Final[int] = 25
    RESET_NEGATIVE: Final[int] = 27
    RESET_HIDDEN: Final[int] = 28
    RESET_STRIKETHROUGH: Final[int] = 29
    RESET_ALL: Final[int] = 0


Fore = AnsiFore()
"""Struct containing ANSI foreground codes."""

Back = AnsiBack()
"""Struct containing ANSI background codes."""

Style = AnsiStyle()
"""Struct containing ANSI style codes."""
