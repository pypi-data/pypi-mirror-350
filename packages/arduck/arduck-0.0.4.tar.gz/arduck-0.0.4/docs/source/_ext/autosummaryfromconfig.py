"""Adds the ability to extract the name of the module to be used in the
autosummary directive from a configuration value.

New options:
    - :fromconfig: config
      the package module name will be extracted fromm the config value.


Typical usage:

    .. autosummary::
        :toctree: _autosummary
        :fromconfig: project

    Will produce a summary of the package named after the string contained
    in the `project` variable inside the conf.py file.
"""

import re
from typing import Any, Callable, Optional

from sphinx.ext import autosummary
from docutils.nodes import Node
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.ext.autosummary.generate import AutosummaryEntry


def patch_autosummary_directive_run_method(
        app: Sphinx,
        func: Callable[[autosummary.Autosummary], list[Node]]
) -> Callable[[autosummary.Autosummary], list[Node]]:
    """Decorator function to patch the run method of the Autosummary directive."""

    def patch(self: autosummary.Autosummary) -> list[Node]:
        """"""

        app_config: dict = {
            config_value.name: config_value.value for config_value in app.config
        }

        if 'fromconfig' in self.options:
            if package_name := app_config.get(self.options['fromconfig'], None):
                self.content = [package_name]
                self.block_text = self.block_text + f'{' ' * 4}tool\n\n'
        output = func(self)
        return output

    if hasattr(func, '__doc__'):
        patch.__doc__ = func.__doc__

    return patch


def patch_find_autosummary_in_lines_function(
        app: Sphinx,
        func: Callable[[list[str], Optional[str], Optional[str]], list[AutosummaryEntry]]
) -> Callable[[list[str], Optional[str], Optional[str]], list[AutosummaryEntry]]:
    """Decorator function to patch the find_autosummary_in_lines function
    of the autosummary.generate module.
    """

    indent: str = ' ' * 4
    app_config: dict = {
        config_value.name: config_value.value for config_value in app.config
    }

    def patch(
            lines: list[str],
            module: Optional[str] = None,
            filename: Optional[str] = None,
    ) -> list[AutosummaryEntry]:
        fromconfig_arg_re = re.compile(r'^\s+:fromconfig:\s*(.*?)\s*$')

        for i, line in enumerate(lines):
            if m := fromconfig_arg_re.match(line):
                conf_value = m.group(1).strip()
                if package_name := app_config.get(conf_value, None):
                    lines[i] = f'{indent}{package_name}\n'

        return func(lines, module, filename)

    if hasattr(func, '__doc__'):
        patch.__doc__ = func.__doc__

    return patch


def apply_autosummary_directive_patch(
        app: Sphinx,
        cls: [autosummary.Autosummary],
) -> autosummary.Autosummary:
    """Applies the Autosummary directive patch."""

    if not cls.option_spec:
        cls.option_spec = {}

    cls.option_spec |= {
        'fromconfig': directives.unchanged,
    }

    cls.run = patch_autosummary_directive_run_method(app, cls.run)

    return cls


def apply_autosummary_function_patch(
        app: Sphinx,
        module: [autosummary.generate],
) -> autosummary.generate:
    """Applies the autosummary.generate.find_autosummary_in_lines function patch."""

    module.find_autosummary_in_lines = patch_find_autosummary_in_lines_function(
        app,
        module.find_autosummary_in_lines,
    )

    return module


def setup(app: Sphinx) -> dict[str, Any]:
    """Sphinx extension entry point.

    Args:
        app:
          Sphinx instance.

    Returns:
        the metadata of the extension.
    """

    app.setup_extension('sphinx.ext.autosummary')

    autosummary.Autosummary = apply_autosummary_directive_patch(
        app,
        autosummary.Autosummary,
    )
    autosummary.generate = apply_autosummary_function_patch(
        app,
        autosummary.generate,
    )

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
