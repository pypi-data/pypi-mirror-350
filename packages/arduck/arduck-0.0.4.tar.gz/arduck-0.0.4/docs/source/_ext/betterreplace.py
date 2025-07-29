"""Adds new functionalities to the docutils replace directive.

New options:
    - :lower:
      converts the substitution reference to lowercase.

    - :upper:
      converts the substitution reference to uppercase.

    - :ltrim:
      whitespace to the left of the substitution reference is removed.

    - :rtrim:
      whitespace to the right of the substitution reference is removed.

    - :trim:
      equivalent to ltrim plus rtrim; whitespace on both sides of the substitution reference is removed.
"""

from typing import Any, Callable

from docutils.nodes import Node
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives import misc
from sphinx.application import Sphinx


def apply_replace_run_patch(
        func: Callable[[misc.Replace], list[Node]]
) -> Callable[[misc.Replace], list[Node]]:
    """Decorator function to patch the run method of the Replace directive."""

    def patch(self: misc.Replace) -> list[Node]:

        if 'lower' in self.options:
            self.content.data = list(map(str.lower, self.content.data))

        if 'upper' in self.options:
            self.content.data = list(map(str.upper, self.content.data))

        if 'ltrim' in self.options:
            self.content.data = list(map(str.ltrim, self.content.data))

        if 'rtrim' in self.options:
            self.content.data = list(map(str.rtrim, self.content.data))

        if 'trim' in self.options:
            self.content.data = list(map(str.trim, self.content.data))

        return func(self)

    if hasattr(func, '__doc__'):
        patch.__doc__ = func.__doc__

    return patch


def apply_replace_patch(
        cls: misc.Replace
) -> misc.Replace:
    """Decorator function to patch the Replace directive."""
    
    if not cls.option_spec:
        cls.option_spec = {}

    cls.option_spec |= {
        'lower': directives.flag,
        'upper': directives.flag,
        'trim': directives.flag,
        'ltrim': directives.flag,
        'rtrim': directives.flag,
    }

    cls.run = apply_replace_run_patch(cls.run)

    return cls


def setup(app: Sphinx) -> dict[str, Any]:
    """Sphinx extension entry point.

    Args:
        app:
          Sphinx instance.

    Returns:
        the metadata of the extension.
    """

    misc.Replace = apply_replace_patch(misc.Replace)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
