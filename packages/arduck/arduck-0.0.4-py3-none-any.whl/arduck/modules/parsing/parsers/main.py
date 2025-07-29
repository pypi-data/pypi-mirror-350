"""Provides a template for the main ArgumentParser of the package."""

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
from collections.abc import Sequence
from datetime import datetime
from typing import override, Optional


from ...ansi import Style
from ... import metadata
from .. import ExtendableArgumentParser, SmartFormatter
from ..parents import VerboseArgumentParser


def _format_package_information() -> str:
    """Returns package information, formatted as follows:

    {package name} {package version} (*)({development status})
    Copyright (c) {year} (*){authors}.
    (*)Maintained by {maintainers}.
    (*)License: {license type}.

    (*)Project URLs:
    {website name} => {website url}.
    ...

    Fields marked with (*) will be omitted if not present in the package metadata.
    """

    authors_dict: dict[str, str] = metadata.authors()

    authors_list: list[str] = []
    for author_name, author_email in authors_dict.items():
        authors_list.append(
            ''.join((
                author_name,
                f' <{author_email}>' if author_email else '',
            ))
        )
    authors_string: str = ', '.join(authors_list)

    maintainers_list: list[str] = []
    for maintainer_name, maintainer_email in metadata.maintainers().items():
        # if a maintainer is also an author, its email address will not be
        # repeated in the maintainers section to avoid redundancy.
        maintainers_list.append(
            ''.join((maintainer_name, f' <{maintainer_email}>'))
            if (
                    maintainer_email and
                    authors_dict.get(maintainer_name, '') != maintainer_email
            )
            else maintainer_name
        )

    # if there is more than one package maintainer,
    # adds 'and' before the last name.
    maintainers_string: str = (
        maintainers_list[0] if len(maintainers_list) < 2 else
        f'{', '.join(maintainers_list[:-1])} and {maintainers_list[-1]}'
    )

    urls_list: list[str] = []
    for website_name, website_url in metadata.project_url().items():
        urls_list.append(
            f'{website_name.capitalize()} => '
            f'{Style.UNDERLINE}{website_url}{Style.RESET_UNDERLINE}.'
        )
    urls_string: str = '\n'.join(urls_list)

    dev_status: str = metadata.development_status()
    license_name: str = metadata.license_type()

    return ''.join((
        f'{metadata.package()} {metadata.version()}'
        f'{f' ({dev_status.lower()})' if dev_status else ''}\n',
        f'Copyright (c) {datetime.now().year}'
        f'{f' {authors_string}' if authors_string else ''}.\n',
        f'Maintained by {maintainers_string}.\n' if maintainers_string else '',
        f'License{'d under the ' if 'license' in license_name.lower() else ' - '}{license_name}.\n'
        if license_name else '',
        f'\nProject URLs:\n{urls_string}' if urls_string else '',
    ))


class MainArgumentParserTemplate(ExtendableArgumentParser):
    """Argument parser that adds basic CLI functionalities.

    New subparser:
        config:
            allows the user to view and modify application settings.

    New flag:
        -V, --version:
            show version information and exit.
    """

    @override
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            formatter_class=SmartFormatter,
            parents=[VerboseArgumentParser()],
            **kwargs,
        )

        self.add_argument(
            '-V', '--version',
            action='version',
            version=_format_package_information(),
        )

    @override
    def parse_args(
            self,
            args: Optional[Sequence[str]] = None,
            namespace: Optional[Namespace] = None,
    ) -> Namespace:
        return super().parse_args(args=args, namespace=namespace)
