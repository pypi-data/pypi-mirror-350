"""Command Line Interface entry point."""

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


from argparse import Namespace
import logging

from jinja2 import Template

from .modules.template import TemplateParameters


logger = logging.getLogger(__name__)


def main(namespace: Namespace) -> None:
    """Main CLI function.

    Args:
        namespace:
          Namespace containing the command line parsing.
    """

    chosen_template: Template = namespace.template
    template_parameters: TemplateParameters = {
        'do_repeat': namespace.repeat,
        'interval_mapping': namespace.interval_mapping,
        'keyboard_layout': namespace.layout,
        'keystrokes': namespace.keystrokes,
        'wpm': namespace.wpm,
    }

    payload = chosen_template.render(**template_parameters)

    namespace.outfile.write(payload)
    namespace.outfile.close()
