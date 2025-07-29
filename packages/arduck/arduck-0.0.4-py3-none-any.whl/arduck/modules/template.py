"""Provides easy access to the package metadata."""

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


from importlib import resources
from pathlib import Path
import shutil
from typing import Literal, TypedDict

from jinja2 import Environment, FileSystemLoader, Template

from ..modules import metadata
from ..tokenizer import Keystroke, SleepInterval


TEMPLATES_DIRECTORY: Path = Path(
    str(resources.files(metadata.package()) / 'templates')
)
ENVIRONMENT = Environment(
    loader=FileSystemLoader(TEMPLATES_DIRECTORY)
)


def btoi_filter(byte: bytes) -> int:
    """"""

    return int.from_bytes(byte)


def encode_filter(value: str, encoding: str) -> bytes:
    """"""

    return value.encode(encoding)


ENVIRONMENT.filters['btoi'] = btoi_filter
ENVIRONMENT.filters['encode'] = encode_filter


class TemplateParameters(TypedDict):
    """Parameters accepted by a template."""

    do_repeat: Literal[False] | int
    interval_mapping: list[tuple[int, SleepInterval]]
    keyboard_layout: str
    keystrokes: list[Keystroke]
    wpm: int


def add(path: Path) -> None:
    """Adds a template to the package collection.

    Args:
        path:
            the template's path.
    """

    shutil.copy(path, TEMPLATES_DIRECTORY)


def enum() -> list[str]:
    """Lists all available templates."""

    return ENVIRONMENT.list_templates()


def get(name: str) -> Template:
    """Loads a template by name.

    Args:
        name:
            the name of the template.
    """

    return ENVIRONMENT.get_template(name)


def remove(name: str) -> None:
    """Removes a template from the package's collection.

    Args:
        name:
            the name of the template to remove.
    """

    (TEMPLATES_DIRECTORY / name).unlink()
