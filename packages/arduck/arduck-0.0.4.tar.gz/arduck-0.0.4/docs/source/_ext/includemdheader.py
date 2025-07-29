"""Adds new functionalities to the docutils include directive.

New options:
    - :header: header
      when including a markdown file, it is possible to select only the
      contents under a certain header.
"""

from pathlib import Path
import re
from typing import Any, Callable

from docutils import io, utils
from docutils.nodes import Node
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives import misc
from sphinx.application import Sphinx


markdown_header_regex = re.compile(
    r'^\s*(?P<level>#{1,6})\s*(?P<title>[\w ]+)\s*$'
)


def apply_include_run_patch(
        func: Callable[[misc.Include], list[Node]]
) -> Callable[[misc.Include], list[Node]]:
    """Decorator function to patch the run method of the Include directive."""

    def patch(self: misc.Include) -> list[Node]:
        if (target_header_title := self.options.get('header')) is None:
            return func(self)

        if not self.state.document.settings.file_insertion_enabled:
            raise self.warning('"%s" directive disabled.' % self.name)

        current_source = self.state.document.current_source

        path = directives.path(self.arguments[0])
        if path.startswith('<') and path.endswith('>'):
            _base = self.standard_include_path
            path = path[1:-1]

        else:
            _base = Path(current_source).parent

        path = utils.relative_path(None, _base / path)

        encoding = self.options.get(
            'encoding', self.state.document.settings.input_encoding
        )
        e_handler = self.state.document.settings.input_encoding_error_handler

        try:
            include_file = io.FileInput(
                source_path=path,
                encoding=encoding,
                error_handler=e_handler,
            )
        except UnicodeEncodeError:
            raise self.severe(
                f'Problems with "{self.name}" directive path:\n'
                f'Cannot encode input file path "{path}" '
                f'(wrong locale?).'
            )
        except OSError as error:
            raise self.severe(
                f'Problems with "{self.name}" directive '
                f'path:\n{io.error_string(error)}.'
            )
        else:
            self.state.document.settings.record_dependencies.add(path)

        header_level = ''
        lines = include_file.readlines()
        self.options['start-line'],  self.options['end-line'] = 0, len(lines)
        for i, line in enumerate(lines):
            if (m := re.match(markdown_header_regex, line)) is not None:
                level, title = m.group('level'), m.group('title')

                if not header_level:
                    if title == target_header_title:
                        header_level = level
                        self.options['start-line'] = i + 1
                else:
                    if len(level) <= len(header_level):
                        self.options['end-line'] = i - 1
                        break

        return func(self)

    if hasattr(func, '__doc__'):
        patch.__doc__ = func.__doc__

    return patch


def apply_replace_patch(
        cls: misc.Include
) -> misc.Include:
    """Decorator function to patch the Include directive."""

    cls.option_spec = misc.Include.option_spec | {
        'header': directives.unchanged,
    }

    cls.run = apply_include_run_patch(cls.run)

    return cls


def setup(app: Sphinx) -> dict[str, Any]:
    """Sphinx extension entry point.

    Args:
        app:
          Sphinx instance.

    Returns:
        the metadata of the extension.
    """

    misc.Include = apply_replace_patch(misc.Include)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
