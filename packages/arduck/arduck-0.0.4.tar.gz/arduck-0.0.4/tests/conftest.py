from importlib import import_module
from importlib.metadata import metadata as importlib_metadata
from pathlib import Path
import tomllib

import pytest


def get_package_name(pyproject_toml: Path) -> str:
    """Returns the package name extracted from the pyproject.toml file.

    Args:
        pyproject_toml:
          path to the pyproject.toml config file.
    """

    with open(pyproject_toml, 'rb') as f:
        data = tomllib.load(f)

    return data['project']['name']


def get_package_metadata(package_name: str) -> dict:
    """Returns the JSON representation of the package metadata.

    For more information, see:
    https://docs.python.org/3/library/importlib.metadata.html#distribution-metadata.

    Args:
        package_name:
          the name of the package from which to extract the metadata.
    """

    return importlib_metadata(package_name).json


@pytest.fixture(autouse=True, scope='session')
def init_global_variables():
    """Initializes global variables used for testing purposed."""

    package_pyproject_path: Path = Path.resolve(
        Path(__file__).parent / '..' / 'pyproject.toml'
    )
    package_name: str = get_package_name(package_pyproject_path)

    pytest.PACKAGE_MODULE = import_module(package_name)
    pytest.PACKAGE_METADATA = get_package_metadata(package_name)


@pytest.fixture(scope='session')
def package():
    """Returns the package that is being tested."""

    return pytest.PACKAGE_MODULE


@pytest.fixture(scope='session')
def metadata():
    """Returns the package metadata."""

    return pytest.PACKAGE_METADATA
