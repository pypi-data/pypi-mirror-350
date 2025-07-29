"""Fixes the :caption: option in the autosummary directive by monkeypatching
the run method of the Autosummary class.

Problem:
    For some reason, when a caption is specified, it is not actually rendered.

    There is a GitHub issue that mentions this:
    https://github.com/sphinx-doc/sphinx/issues/7490.
"""

from typing import Any, Callable

from docutils import nodes
from docutils.nodes import Node
from sphinx.application import Sphinx
from sphinx.ext import autosummary


def patch_autosummary_directive_run_method(
        func: Callable[[autosummary.Autosummary], list[Node]]
) -> Callable[[autosummary.Autosummary], list[Node]]:
    """Decorator function to patch the run method of the Autosummary directive."""

    def patch(self: autosummary.Autosummary) -> list[Node]:
        nodes_list = func(self)

        if caption := self.options.get('caption'):
            section_node = nodes.section(ids=[nodes.make_id(caption)])
            section_node += nodes.title(text=caption)
            section_node += nodes_list

            nodes_list = [section_node]

        return nodes_list

    if hasattr(func, '__doc__'):
        patch.__doc__ = func.__doc__

    return patch


def apply_autosummary_directive_patch(
        cls: [autosummary.Autosummary],
) -> autosummary.Autosummary:
    """Applies the Autosummary directive patch."""

    cls.run = patch_autosummary_directive_run_method(
        cls.run
    )

    return cls


def setup(app: Sphinx) -> dict[str, Any]:
    """Sphinx extension entry point.

    Args:
        app:
          Sphinx instance.

    Returns:
        the metadata of the extension.
    """

    app.setup_extension('sphinx.ext.autosummary')
    apply_autosummary_directive_patch(autosummary.Autosummary)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
