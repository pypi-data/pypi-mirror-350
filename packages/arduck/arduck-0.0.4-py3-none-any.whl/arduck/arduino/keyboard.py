"""Contains keyboard library constants."""

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


# https://docs.arduino.cc/language-reference/en/functions/usb/Keyboard/keyboardBegin/#Keyboard%20layouts.
LAYOUTS: dict[str, str] = {
    'dk': 'da_DK',
    'de': 'de_DE',
    'us': 'en_US',
    'es': 'es_ES',
    'fr': 'fr_FR',
    'hu': 'hu_HU',
    'it': 'it_IT',
    'pt': 'pt_PT',
    'se': 'sv_SE',
}

# https://docs.arduino.cc/language-reference/en/functions/usb/Keyboard/keyboardModifiers/.
SPECIAL_KEYS: dict[str, str] = {
    # keyboard modifiers.
    'LEFT_CTRL': 'KEY_LEFT_CTRL',
    'LEFT_SHIFT': 'KEY_LEFT_SHIFT',
    'LEFT_ALT': 'KEY_LEFT_ALT',
    'LEFT_GUI': 'KEY_LEFT_GUI',
    'RIGHT_CTRL': 'KEY_RIGHT_CTRL',
    'RIGHT_SHIFT': 'KEY_RIGHT_SHIFT',
    'RIGHT_ALT': 'KEY_RIGHT_ALT',
    'RIGHT_GUI': 'KEY_RIGHT_GUI',

    # within the alphanumeric cluster.
    'TAB': 'KEY_TAB',
    'CAPS_LOCK': 'KEY_CAPS_LOCK',
    'BACKSPACE': 'KEY_BACKSPACE',
    'RETURN': 'KEY_RETURN',
    'MENU': 'KEY_MENU',

    # navigation cluster.
    'INSERT': 'KEY_INSERT',
    'DELETE': 'KEY_DELETE',
    'HOME': 'KEY_HOME',
    'END': 'KEY_END',
    'PAGE_UP': 'KEY_PAGE_UP',
    'PAGE_DOWN': 'KEY_PAGE_DOWN',
    'UP_ARROW': 'KEY_UP_ARROW',
    'DOWN_ARROW': 'KEY_DOWN_ARROW',
    'LEFT_ARROW': 'KEY_LEFT_ARROW',
    'RIGHT_ARROW': 'KEY_RIGHT_ARROW',

    # numeric keypad.
    'NUM_LOCK': 'KEY_NUM_LOCK',
    'KP_SLASH': 'KEY_KP_SLASH',
    'KP_ASTERISK': 'KEY_KP_ASTERISK',
    'KP_MINUS': 'KEY_KP_MINUS',
    'KP_PLUS': 'KEY_KP_PLUS',
    'KP_ENTER': 'KEY_KP_ENTER',
    'KP_1': 'KEY_KP_1',
    'KP_2': 'KEY_KP_2',
    'KP_3': 'KEY_KP_3',
    'KP_4': 'KEY_KP_4',
    'KP_5': 'KEY_KP_5',
    'KP_6': 'KEY_KP_6',
    'KP_7': 'KEY_KP_7',
    'KP_8': 'KEY_KP_8',
    'KP_9': 'KEY_KP_9',
    'KP_0': 'KEY_KP_0',
    'KP_DOT': 'KEY_KP_DOT',

    # escape and function keys.
    'ESC': 'KEY_ESC',
    'F1': 'KEY_F1',
    'F2': 'KEY_F2',
    'F3': 'KEY_F3',
    'F4': 'KEY_F4',
    'F5': 'KEY_F5',
    'F6': 'KEY_F6',
    'F7': 'KEY_F7',
    'F8': 'KEY_F8',
    'F9': 'KEY_F9',
    'F10': 'KEY_F10',
    'F11': 'KEY_F11',
    'F12': 'KEY_F12',
    'F13': 'KEY_F13',
    'F14': 'KEY_F14',
    'F15': 'KEY_F15',
    'F16': 'KEY_F16',
    'F17': 'KEY_F17',
    'F18': 'KEY_F18',
    'F19': 'KEY_F19',
    'F20': 'KEY_F20',
    'F21': 'KEY_F21',
    'F22': 'KEY_F22',
    'F23': 'KEY_F23',
    'F24': 'KEY_F24',

    # function control keys.
    'PRINT_SCREEN': 'KEY_PRINT_SCREEN',
    'SCROLL_LOCK': 'KEY_SCROLL_LOCK',
    'PAUSE': 'KEY_PAUSE',
}
