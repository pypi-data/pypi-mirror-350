from datetime import datetime
from importlib import import_module
import os
from pathlib import Path
import sys
import tomllib

from sphinx.application import Sphinx


sys.path.append(os.path.abspath('./_ext'))


def get_package_name(pyproject_toml: Path) -> str:
    """Returns the project name contained in the pyproject.toml file.

    Args:
        pyproject_toml:
          path to the pyproject.toml configuration file.
    """

    with open(pyproject_toml, 'rb') as f:
        data = tomllib.load(f)

    return data['project']['name']


pyproject_path: Path = (
    Path.resolve(Path(__file__).parent / '..' / '..' / 'pyproject.toml')
)
package = import_module(get_package_name(pyproject_path))


# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = package.__package__
author = package.__author__
release = package.__version__
version = '.'.join(release.split('.')[:2])

copyright = f'{datetime.now().year} {author}'


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

builtin_extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

external_extensions = [
    'sphinxarg.ext',
    'sphinx_autodoc_typehints',
    'sphinx_rtd_theme',
]

custom_extensions = [
    'autosummarycaption',
    'autosummaryfromconfig',
    'betterreplace',
    'includemdheader',
    'metadata',
    'projectmetadata',
]

extensions = builtin_extensions + external_extensions + custom_extensions

exclude_patterns = []
source_suffix = ['.rst']
templates_path = ['_templates']


add_module_names = False
autoclass_content = 'class'
autodoc_class_signature = 'mixed'
autodoc_default_options = {
    # 'exclude-members': '__weakref__',
    'inherited-members': False,
    'members': True,
    'member-order': 'bysource',
    'private-members': False,
    'special-members': '__author__, __version__, __new__',
    'undoc-members': True,
}
autodoc_docstring_signature = True
autodoc_inherit_docstrings = True
autodoc_typehints = 'signature'
autodoc_typehints_format = 'short'

autosummary_generate = True
autosummary_generate_overwrite = True
autosummary_ignore_module_all = False
autosummary_imported_members = False

napoleon_google_docstring = True
# napoleon_use_param = True

typehints_fully_qualified = False
typehints_use_signature = True
typehints_use_signature_return = True

intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = ['_static']
html_theme = 'sphinx_rtd_theme'


def setup(app: Sphinx) -> None:
    """Sphinx config entry point.

    Args:
        app:
          Sphinx instance.
    """

    pass
