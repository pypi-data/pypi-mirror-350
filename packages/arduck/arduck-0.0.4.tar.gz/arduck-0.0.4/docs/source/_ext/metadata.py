"""Provides easy access to the package metadata by adding new configuration
values to app.config.

The package from which the metadata is extracted is the one whose name
is the same as the value of the 'project' variable defined in the namespace
of the project’s configuration.

New configuration values:
    - metadata_project_json:
      contains the package metadata as a JSON dictionary.
    - metadata_project_development_status:
      contains the package development status and its associated stage index,
      extracted from the "Development Status" classifier (if present).
    - metadata_project_license_type:
      contains the package license type, extracted from the "License" classifier
      (if present).
    - metadata_project_urls:
      contains a dict mapping the project websites with their corresponding urls.
"""

from importlib.metadata import metadata, PackageNotFoundError
import logging
from operator import methodcaller
from typing import Any

from sphinx.application import Sphinx


type JSONPackageMetadata = dict[str, str | list[str]]

logger = logging.getLogger(__name__)


def get_package_metadata(package_name: str) -> JSONPackageMetadata:
    """Returns the package metadata in JSON format.

    For more information, see:
    https://docs.python.org/3/library/importlib.metadata.html#distribution-metadata.

    Args:
        package_name:
          the name of the package.

    Raises:
        PackageNotFoundError:
          the specified package was not found.
    """

    try:
        package_metadata: JSONPackageMetadata = (
            metadata(package_name).json
        )
    except PackageNotFoundError:
        logger.critical('%r package not found.', package_name)
        raise

    return package_metadata


def get_package_development_status(package_metadata: JSONPackageMetadata) -> tuple[int, str]:
    """Returns the package development status and its associated stage index.

    The status is extracted from the "Development Status" classifier (if present).

    Common possible return values:
        - 1, Planning
        - 2, Pre-Alpha
        - 3, Alpha
        - 4, Beta
        - 5, Production/Stable
        - 6, Mature
        - 7, Inactive

    Args:
        package_metadata:
          package metadata dump in JSON format.
    """

    for classifier_type, classifier_body in map(
            methodcaller('split', ' :: ', 1),
            package_metadata['classifier'],
    ):
        if classifier_type == 'Development Status':
            status_number, status_literal = classifier_body.split(' - ')

            return int(status_number), status_literal

    return 0, ''


def get_package_license_type(package_metadata: JSONPackageMetadata) -> str:
    """Returns the package license type.

    The package license type is extracted from the "License" classifier (if present).

    Args:
        package_metadata:
          package metadata dump in JSON format.
    """

    for classifier_type, classifier_body in map(
            methodcaller('split', ' :: ', 1),
            package_metadata['classifier'],
    ):
        if classifier_type == 'License':
            return classifier_body.split(' :: ')[-1]

    return ''


def get_package_urls(package_metadata: JSONPackageMetadata) -> dict[str, str]:
    """Returns a dict mapping the project websites with their corresponding urls.

    Args:
        package_metadata:
          package metadata dump in JSON format.
    """

    package_project_url_field: list[str] = (
        package_metadata['project_url']
    )

    package_project_urls: dict[str, str] = {}

    # Raymond Hettinger (2011, December 11). python map (...). StackOverflow.
    # https://stackoverflow.com/a/8461254.
    for website_name, website_url in map(
            methodcaller('split', ', '),
            package_project_url_field,
    ):
        package_project_urls[website_name] = website_url

    return package_project_urls


def setup(app: Sphinx) -> dict[str, Any]:
    """Sphinx extension entry point.

    Args:
        app:
          Sphinx instance.

    Returns:
        the metadata of the extension.
    """

    app_config: dict = {
        config_value.name: config_value.value for config_value in app.config
    }
    package_name: str = app_config['project']
    package_metadata: JSONPackageMetadata = get_package_metadata(package_name)

    app.add_config_value(
        name='metadata_project_json',
        default=package_metadata,
        rebuild='',
        types=JSONPackageMetadata.__value__,
    )

    app.add_config_value(
        name='metadata_project_development_status',
        default=get_package_development_status(package_metadata),
        rebuild='',
        types=list,
    )

    app.add_config_value(
        name='metadata_project_license_type',
        default=get_package_license_type(package_metadata),
        rebuild='',
        types=str,
    )

    app.add_config_value(
        name='metadata_project_urls',
        default=get_package_urls(package_metadata),
        rebuild='',
        types=dict[str, str],
    )

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
