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


import email.policy
from email import message_from_string
import logging
from importlib.metadata import (
    metadata,
    PackageMetadata,
    PackageNotFoundError,
)
from operator import methodcaller
from typing import Literal


logger = logging.getLogger(__name__)


def package() -> str:
    """Returns the package name."""

    return __package__.split('.', maxsplit=1)[0]


package_name = package()

try:
    package_metadata: PackageMetadata = metadata(package_name)
except PackageNotFoundError:
    logger.critical('%r package not found.', package_name)
    raise


def version() -> str:
    """Returns the package version."""

    return package_metadata.get_all('Version', [''])[0]


def summary() -> str:
    """Returns the package summary."""

    return package_metadata.get_all('Summary', [''])[0]


def readme() -> str:
    """Returns the contents of the package README.md file."""

    return package_metadata.get_all('Description', [''])[0]


def license() -> str:
    """Returns the package license."""

    return package_metadata.get_all('License', [''])[0]


def authors() -> dict[str, str]:
    """Returns a dictionary mapping package authors to
    their corresponding email addresses.
    """

    return _field_with_email('Author')


def maintainers() -> dict[str, str]:
    """Returns a dictionary mapping package maintainers to
    their corresponding email addresses.
    """

    return _field_with_email('Maintainer')


def classifiers() -> list[str]:
    """Returns a list containing package classifiers.

    For a comprehensive list of classifiers see: https://pypi.org/classifiers.
    """

    return package_metadata.get_all('Classifier', [])


def development_status() -> str | None:
    """Returns the package development status.

    The status is extracted from the "Development Status" classifier (if present).

    Common possible return values:
        - Planning
        - Pre-Alpha
        - Alpha
        - Beta
        - Production/Stable
        - Mature
        - Inactive
    """

    for classifier_type, classifier_body in map(
            methodcaller('split', ' :: ', 1),
            classifiers(),
    ):
        if classifier_type == 'Development Status':
            _status_number, status_literal = classifier_body.split(' - ')

            return status_literal

    return None


def license_type() -> str | None:
    """Returns the package license type.

    The package license type is extracted from the "License" classifier (if present).
    """

    for classifier_type, classifier_body in map(
            methodcaller('split', ' :: ', 1),
            classifiers(),
    ):
        if classifier_type == 'License':
            return classifier_body.split(' :: ')[-1]

    return None


def project_url() -> dict[str, str]:
    """Returns a dictionary mapping the project websites
    with their corresponding urls.
    """

    urls: dict[str, str] = {}
    project_urls: list[str] = (
        package_metadata.get_all('Project-URL', [])
    )

    # Raymond Hettinger (2011, December 11). python map (...). StackOverflow.
    # https://stackoverflow.com/a/8461254.
    for website_name, website_url in map(
            methodcaller('split', ', '),
            project_urls,
    ):
        urls[website_name] = website_url

    return urls


def _field_with_email(field: Literal['Author', 'Maintainer']) -> dict[str, str]:
    """Returns a dictionary mapping names to their corresponding email addresses
    from a specific metadata field.

    Args:
        field:
            the target metadata field.
    """

    field_metadata: dict[str, str] = {}

    # for more information on the fields structure see:
    # https://packaging.python.org/en/latest/specifications/declaring-project-metadata/#authors-maintainers.
    name_fields: list[str] = (
        package_metadata.get_all(field, [])
    )
    fields_with_emails: list[str] = (
        package_metadata.get_all(f'{field}-email', [])
    )

    for name_field in name_fields:
        field_metadata[name_field] = ''

    for email_field in fields_with_emails:
        # sinoroc (2023, March 21). importlib.metadata (...). StackOverflow.
        # https://stackoverflow.com/a/75803208.
        email_field_message = message_from_string(
            f'To: {email_field}',
            policy=email.policy.default,
        )

        for entry in email_field_message['to'].addresses:
            if not (display_name := entry.display_name):
                # guess the name from the username portion of the email address.
                display_name: str = ' '.join(
                        map(str.capitalize, entry.username.split('.'))
                    )

            field_metadata[display_name] = entry.addr_spec

    return field_metadata
