
# 📦 arduck

[![License: GPL v3](https://img.shields.io/badge/License-GPL_v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.html)
![Python version: 3.12+](https://img.shields.io/badge/python-3.12+-blue)
[![Common Changelog](https://common-changelog.org/badge.svg)](https://common-changelog.org)


## Overview

This package provides a simple and flexible way to generate keystroke injection scripts. It supports a variety of [boards](https://docs.arduino.cc/language-reference/en/functions/usb/Keyboard/#Compatible%20Hardware) and [keyboard layouts](https://docs.arduino.cc/language-reference/en/functions/usb/Keyboard/keyboardBegin/#Keyboard%20layouts).

Rather than relying on expensive proprietary devices (rubberducky _cough cough_), you can use any Arduino-compatible board that supports the [Keyboard.h](https://docs.arduino.cc/language-reference/en/functions/usb/Keyboard) library.


## Installation

Install the package from PyPI by running:

```bash
$ pip install arduck
```


## Usage

Start generating payloads right away with the `duck` console script:

```bash
$ duck "helloworld!\n"
```

This will create a `sketch.ino` file in the current working directory.
Compiling and uploading the code to an Arduino board will make it emulate the keystrokes when plugged into a computer.
Be ready to quickly disconnect the board to avoid **triggering the payload on your machine**.


### Special Keys

To inject _special keys_ (e.g. `CAPS_LOCK`), wrap them in `<>`.
When specifying a _special key_, the `KEY_` prefix can be omitted.

```bash
$ duck "<F1>"
```

All default special keys are listed [here](https://www.arduino.cc/reference/en/language/functions/usb/keyboard/keyboardmodifiers/#_keyboard_modifiers).
Note that some keyboards may have support for other non-standard keys.


### Key Combinations

To emulate pressing multiple keys at once wrap them in `<>`, separated by a `+`.

```bash
$ duck "<LEFT_GUI+r>calc.exe\n"
```


### Add delays

An optional delay in milliseconds can be added in between strings in the input.

```bash
$ duck "<LEFT_GUI+r>" 700 "notepad.exe\n" 500 "hello\n" "world!\n"
```


### More Features

Check out the official documentation for a more comprehensive list of features.


## A Word of Caution

Be careful when using and testing arduino scripts that emulate keyboard and mouse presses, because they might make it difficult to program your board.
And please, always ask for permission from the owner of the machine before plugging in any external devices. Keep in mind that, if abused, this tool has the potential to cause serious harm.

This software is distributed ‘as is’ and without warranties of any kind, either express or implied. Use of the software is at your own risk.


## Documentation

- [Official Documentation](https://x55xaa.github.io/arduck)
- [CHANGELOG](https://github.com/x55xaa/arduck/blob/main/CHANGELOG.md)
