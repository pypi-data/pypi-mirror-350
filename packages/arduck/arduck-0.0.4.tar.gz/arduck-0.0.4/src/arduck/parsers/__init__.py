"""Contains all the argument parsers used by this package.

Each module should contain a `_construct()` function that returns an
instance of the module's argument parser. This function will be used as the `:func:`
argument for the `argparse` directive in the docs.

See https://sphinx-argparse.readthedocs.io/en/stable for more information.
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


from .main import MainArgumentParser


__all__ = ['MainArgumentParser']
