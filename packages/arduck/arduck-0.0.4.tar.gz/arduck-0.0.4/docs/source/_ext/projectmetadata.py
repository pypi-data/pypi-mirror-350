"""Adds new Sphinx directives and features to manage and display package metadata.

The Python package from which the metadata is pulled is the one whose name is
the same as the value of the 'project' variable defined in the namespace of the
project’s configuration.


New directives:
    - .. projecturls::
      Adds a toc tree full of project urls extracted from the Project-URL
      entry in the package metadata.

    - .. projectstatusalert::
      Displays an admonition if the development status of the Python
      package (extracted from the package classifiers) is equal or below a
      certain development stage.

      For more information on development status classifiers, see:
      https://pypi.org/classifiers.


New replace directives:
    - |author|
      the package author.
    - |license|
      the package license (e.g. Creative Commons).
    - |summary|
      the package summary.


For more information on package metadata, see:
https://docs.python.org/3/library/importlib.metadata.html#overview.
"""

import logging
from typing import Any

from docutils import nodes
from docutils.nodes import Node
from docutils.parsers.rst import directives
from docutils.statemachine import StringList
from sphinx import addnodes
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective
from sphinx.util.typing import OptionSpec


type PackageMetadata = dict[str, str | list[str]]

logger = logging.getLogger(__name__)


# taken from: https://pypi.org/classifiers/.
DEV_STATUS_MAPPING: dict[int, tuple[str]] = {
    1: ('Planning',),
    2: ('Pre-Alpha',),
    3: ('Alpha',),
    4: ('Beta',),
    5: ('Production/Stable', 'Production', 'Stable'),
    6: ('Mature',),
    7: ('Inactive',),
}


class ProjectURLNode(nodes.Element):
    pass


class DevStatusAlertNode(nodes.Element):
    pass


class ProjectURLsDirective(SphinxDirective):
    """Sphinx directive that add a toc tree of project urls
    extracted from the specified Python package metadata.

    Args:
        caption:
          optional caption for the toc tree.
        hidden:
          optional flag to hide the toc tree.
    """

    app: Sphinx

    has_content: bool = True

    optional_arguments = 1
    required_arguments = 0

    option_spec: OptionSpec = {
        'caption': directives.unchanged_required,
        'hidden': directives.flag,
    }

    def run(self) -> list[Node]:
        """Sphinx Directive entry point."""

        if self.env.docname != self.env.config.master_doc:
            return []

        body, indent = StringList(['.. toctree::']), ' ' * 4

        if 'caption' in self.options:
            body.append(StringList([f'{indent}:caption: {self.options['caption']}']))

        if 'hidden' in self.options:
            body.append(StringList([f'{indent}:hidden:']))

        body.append(StringList([f'{indent}\n']))
        for website_name, website_url in (
                self.app.config['metadata_project_urls']
                if 'metadata_project_urls' in self.app.config
                else {}
        ).items():
            body.append(StringList([f'{indent}{website_name} <{website_url}>']))

        for line in self.content:
            body.append(StringList([f'{indent}{line}']))

        body.append(StringList(['\n', '\n']))

        node = addnodes.only(expr='html')
        content_node = nodes.paragraph(rawsource=str(body))
        node += content_node
        self.state.nested_parse(
            StringList(body),
            self.content_offset,
            content_node,
        )

        return [node]


class DevStatusAlertDirective(SphinxDirective):
    """Displays an admonition if the development status of the Python
      package (extracted from the package classifiers) is equal or below a
      certain development stage.

      Options:
        :title:
          optional admonition title.
          default title: Development Status
        :body:
          optional admonition body. The strings %(index)d and %(literal)s will
          be replaced by the package development status index and literal
          string (e.g. alpha, beta, ...).
        :status:
          the threshold status. can either be a number or a string.
    """

    optional_arguments = 2
    required_arguments = 1

    option_spec: OptionSpec = {
        'title': directives.unchanged,
        'body': directives.unchanged,
    }

    def run(self) -> list[Node]:
        """Sphinx Directive entry point."""

        node = DevStatusAlertNode()
        node.document = self.state.document
        self.set_source_info(node)

        if title := self.options.get('title'):
            node['title'] = title

        if body := self.options.get('body'):
            node['body'] = body

        node['development_status'] = self.arguments[0]

        return [node]


def process_devstatusalert_nodes(app: Sphinx, doctree: nodes.document, docname: str) -> None:
    """Converts DevStatusAlertNodes into admonitions warning the user if the
    package status is below or equal to a certain development stage.

    The package from which the project urls are extracted is the one whose name
    is the same as the value of the 'project' variable defined in the namespace
    of the project’s configuration.

    Args:
        app:
          Sphinx instance.
        doctree:
          the doctree of the file.
        docname:
          the name of the source file.
    """

    project_development_status = (
        app.config['metadata_project_development_status']
    )

    for node in list(doctree.findall(DevStatusAlertNode)):
        if 'development_status' not in node:
            node.replace_self([])
            continue

        try:
            status_index = int(node['development_status'])

        except ValueError:
            status_literal = node['development_status']

            status_index = None
            for index, literals in DEV_STATUS_MAPPING.items():
                if status_literal.lower() in map(str.lower, literals):
                    status_index = index
                    break

            if status_index is None:
                logger.warning(
                    '[%s] development status literal %r does '
                    'not map to any development status index.',
                    __name__, status_literal,
                )

                node.replace_self([])
                return

        if project_development_status[0] > status_index:
            node.replace_self([])
            continue

        admonition_node = nodes.admonition('')
        admonition_node += nodes.title(
            text=node.get('title', 'Development Status') % {
                 'index': project_development_status[0],
                 'literal': project_development_status[1].lower(),
             }
        )
        admonition_node += nodes.paragraph(
            text=node.get(
                'body',
                'Lorem ipsum dolor sit amet, '
                'consectetur adipiscing elit, '
                'sed do eiusmod tempor incididunt '
                'ut labore et dolore magna aliqua.'
            ) % {
                 'index': project_development_status[0],
                 'literal': project_development_status[1].lower(),
             }

        )

        node.replace_self([admonition_node])


def add_global_rep(app: Sphinx, docname: str, source: list[str]) -> None:
    """Adds some special replace directives at the end of every source file,
    and makes sure that the default ones (e.g. project) work as intended.

    - |author|:
        the package author.
    - |license|:
        the package license (e.g. Creative Commons).
    - |summary|:
        the package summary string.

    Args:
        app:
          Sphinx instance.
        docname:
          the name of the source file.
        source:
          a list whose single element is the contents of the source file.
    """

    app_config: dict = {
        config_value.name: config_value.value for config_value in app.config
    }

    default_repl_fix = '\n'.join((
        f'.. |project| replace:: {app_config.get('project', '|project|')}',
        f'.. |release| replace:: {app_config.get('release', '|release|')}',
        f'.. |version| replace:: {app_config.get('version', '|version|')}',
    ))

    custom_rst_epilog = '\n'.join((
        f'.. |author| replace:: {app_config.get('author', '|author|')}',
        f'.. |license| replace:: {app_config.get('metadata_project_license_type', '|license|')}',
        f'.. |summary| replace:: {app_config.get('metadata_project_json', {}).get('summary', '|summary|')}',
        '    :lower:',
    ))

    repl_source = '\n'.join((
        *source,
        default_repl_fix,
        custom_rst_epilog,
    )) + '\n'

    source.insert(0, repl_source)
    source.pop()


def setup(app: Sphinx) -> dict[str, Any]:
    """Sphinx extension entry point.

    Args:
        app:
          Sphinx instance.

    Returns:
        the metadata of the extension.
    """

    pud = ProjectURLsDirective
    pud.app = app

    app.setup_extension('metadata')
    app.add_directive('projecturls', ProjectURLsDirective)

    app.add_node(DevStatusAlertNode)
    app.add_directive('devstatusalert', DevStatusAlertDirective)
    app.connect('doctree-resolved', process_devstatusalert_nodes)

    app.connect('source-read', add_global_rep)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
