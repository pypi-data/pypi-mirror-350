import collections
import csv
import io
import json
import os
from collections import OrderedDict

import sphinxcontrib.jsonschema
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.parsers.rst.directives.admonitions import Note
from docutils.parsers.rst.directives.tables import CSVTable
from docutils.parsers.rst.roles import set_classes
from docutils.transforms import Transform
from docutils.utils import SystemMessagePropagation, new_document
from jsonpointer import resolve_pointer
from sphinx import addnodes
from sphinx.builders.gettext import MessageCatalogBuilder
from sphinx.directives.code import LiteralInclude


from myst_parser.config.main import MdParserConfig
from myst_parser.mdit_to_docutils.base import make_document
from myst_parser.mdit_to_docutils.sphinx_ import SphinxRenderer
from myst_parser.parsers.mdit import create_md_parser


# to_docutils was removed in myst-parser>=0.18 so we recreate it here.
def to_docutils(text, document=None):
    # Code is similar to MystParser.parse and myst_parser.parsers.docutils_.Parser.parse.
    parser = create_md_parser(MdParserConfig(), SphinxRenderer)
    if not document:
        document = make_document()
    parser.options["document"] = document
    return parser.render(text)


# Based on positive_int_list from docutils
def nonnegative_int_list(argument):
    """
    Converts a space- or comma-separated list of values into a Python list
    of integers.
    (Directive option conversion function.)

    Raises ValueError for non-positive-integer values.
    """
    if ',' in argument:
        entries = argument.split(',')
    else:
        entries = argument.split()
    return [directives.nonnegative_int(entry) for entry in entries]


def flatten_dict(obj, path, result, recursive=False):
    if hasattr(obj, 'items'):
        for key, value in obj.items():
            if isinstance(value, dict):
                if recursive:
                    flatten_dict(value, path + '/' + key, result, recursive=recursive)
            elif isinstance(value, list):
                if isinstance(value[0], dict):
                    if recursive:
                        for num, sub_value in enumerate(value):
                            flatten_dict(sub_value, path + '/' + key + '/' + str(num), result, recursive=recursive)
                else:
                    result[path + '/' + key] = ", ".join(value)
            else:
                result[path + '/' + key] = value


class JSONInclude(LiteralInclude):
    option_spec = {
        'jsonpointer': directives.unchanged,
        'expand': directives.unchanged,
        'exclude': directives.unchanged,
        'include_only': directives.unchanged,
        'title': directives.unchanged,
    }

    def get_filename_and_pointed(self):
        env = self.state.document.settings.env
        dirname = os.path.dirname(env.doc2path(env.docname, base=None))
        relpath = os.path.join(dirname, self.arguments[0])
        abspath = os.path.join(env.srcdir, relpath)
        if not os.access(abspath, os.R_OK):
            raise self.warning('JSON file not readable: %s' %
                               self.arguments[0])

        with open(abspath) as fp:
            json_obj = json.load(fp, object_pairs_hook=OrderedDict)
        filename = str(self.arguments[0]).split("/")[-1].replace(".json", "")
        pointed = resolve_pointer(json_obj, self.options['jsonpointer'])
        return filename, pointed

    def run(self):
        filename, pointed = self.get_filename_and_pointed()

        try:
            title = self.options['title']
        except KeyError:
            title = filename

        # Remove the items mentioned in exclude
        if self.options.get('exclude'):
            for item in self.options['exclude'].split(","):
                try:
                    del pointed[item.strip()]
                except KeyError:
                    pass

        if self.options.get('include_only'):
            for node in list(pointed):
                if not (node in self.options.get('include_only')):
                    del pointed[node]

        code = json.dumps(pointed, indent='    ')
        # Ideally we would add the below to a data-expand element, but I can't see how to do this,
        # so using classes for now...
        class_list = self.options.get('class', [])
        class_list.append('file-' + title)
        expand = str(self.options.get("expand", "")).split(",")
        class_list = class_list + ['expandjson expand-{0}'.format(s.strip()) for s in expand]
        literal = nodes.literal_block(code, code)
        literal['language'] = 'json'
        container = nodes.container(classes=class_list)
        container += literal
        return [container]


class JSONIncludeQuote(JSONInclude):
    def run(self):
        filename, pointed = self.get_filename_and_pointed()
        block_quote = nodes.block_quote('')
        block_quote += parse_markdown(pointed, document=self.state.document)
        return [block_quote]


class CSVTableNoTranslate(CSVTable):
    option_spec = CSVTable.option_spec.copy()
    option_spec['included_cols'] = nonnegative_int_list

    def parse_csv_data_into_rows(self, csv_data, dialect, source):
        rows, max_cols = super().parse_csv_data_into_rows(csv_data, dialect, source)
        if 'included_cols' not in self.options:
            return rows, max_cols

        new_rows = []
        for row in rows:
            try:
                new_rows.append([row[i] for i in self.options['included_cols']])
            except IndexError:
                error = self.state_machine.reporter.error(
                    'One or more indexes of included_cols are not valid. '
                    'The CSV data does not contain that many columns.')
                raise SystemMessagePropagation(error)

        return new_rows, len(self.options['included_cols'])

    def run(self):
        returned = super().run()

        if isinstance(self.state.document.settings.env.app.builder, MessageCatalogBuilder):
            # docutils.parsers.rst.directives.tables.CSVTable.run() returns the nodes.table() node as the first node.
            table_node = returned[0]

            def is_text_element(node):
                return isinstance(node, nodes.TextElement)

            # sphinx.util.nodes.is_translatable() returns True for TextElement unless node['translatable'] is False.
            for node in table_node.traverse(is_text_element):
                node['translatable'] = False

        return returned


class JSONIncludeFlat(CSVTableNoTranslate):
    option_spec = CSVTable.option_spec.copy()
    option_spec['jsonpointer'] = directives.unchanged
    option_spec['title'] = directives.unchanged
    option_spec['exclude'] = directives.unchanged
    option_spec['include_only'] = directives.unchanged
    option_spec['recursive'] = directives.flag
    option_spec['ignore_path'] = directives.unchanged

    def make_title(self):
        return None, []

    def get_csv_data(self):
        env = self.state.document.settings.env
        dirname = os.path.dirname(env.doc2path(env.docname, base=None))
        relpath = os.path.join(dirname, self.arguments[0])
        abspath = os.path.join(env.srcdir, relpath)
        if not os.access(abspath, os.R_OK):
            raise self.warning('JSON file not readable: %s' %
                               self.arguments[0])

        with open(abspath) as fp:
            json_obj = json.load(fp, object_pairs_hook=OrderedDict)
        pointed = resolve_pointer(json_obj, self.options['jsonpointer'])
        if self.options.get('exclude'):
            for item in self.options['exclude'].split(","):
                try:
                    del pointed[item.strip()]
                except KeyError:
                    pass
        if self.options.get('include_only'):
            for node in list(pointed):
                if not (node in self.options.get('include_only')):
                    del pointed[node]
        csv_data = []

        ignore_path = self.options.get('ignore_path', ' ')

        if isinstance(pointed, dict):
            result = collections.OrderedDict()
            flatten_dict(pointed, self.options['jsonpointer'], result, 'recursive' in self.options)
            if ignore_path:
                csv_data.append([heading.replace(ignore_path, "") for heading in result.keys()])
            else:
                csv_data.append(result.keys())
            csv_data.append(list(result.values()))

        if isinstance(pointed, list):
            for row in pointed:
                result = collections.OrderedDict()
                flatten_dict(row, self.options['jsonpointer'], result, 'recursive' in self.options)
                csv_data.append(list(result.values()))
            if ignore_path:
                csv_data.insert(0, [heading.replace(ignore_path, "") for heading in result.keys()])
            else:
                csv_data.insert(0, result.keys())

        output = io.StringIO()
        output_csv = csv.writer(output)
        for line in csv_data:
            output_csv.writerow(line)
        self.options['header-rows'] = 1
        return output.getvalue().splitlines(), abspath


class DirectoryListDirective(Directive):
    option_spec = {
        'path': directives.unchanged,
        'url': directives.unchanged,
    }

    def run(self):
        bl = nodes.bullet_list()
        for fname in os.listdir(self.options.get('path')):
            bl += nodes.list_item('', nodes.paragraph('', '', nodes.reference('', '',
                                  nodes.Text(fname),
                                  internal=False,
                                  refuri=self.options.get('url') + fname, anchorname='')))
        return [bl]


def parse_markdown(text, document=None):
    if document:
        document = new_document(None, document.settings)
    return to_docutils(text, document=document).children[:]


class MarkdownDirective(Directive):
    has_content = True

    def run(self):
        text = '\n'.join(self.content)
        return parse_markdown(text, document=self.state.document)


class LiteralAndParsedMarkdownDirective(Directive):
    has_content = True

    def run(self):
        text = '\n'.join(self.content)
        return [
            nodes.paragraph('', '', nodes.Text('Source:')),
            nodes.literal_block(text, text),
            nodes.paragraph('', '', nodes.Text('Output:')),
        ] + parse_markdown(text, document=self.state.document)


def type_format_simple(prop):
    prop_type = prop.attributes.get('type')
    if prop.format:
        return prop.format
    elif isinstance(prop_type, list) and len(prop_type) == 2 and prop_type[1] == 'null':
        return prop_type[0]
    else:
        return prop.type


class JSONSchemaTitlesDirective(sphinxcontrib.jsonschema.JSONSchemaDirective):
    headers = ['Title', 'Description', 'Type', 'Required']
    widths = [1, 3, 1, 1]
    option_spec = {
        'child': directives.unchanged,
    }
    child = None

    def make_nodes(self, schema):
        child = self.options.get('child')
        if child:
            for prop in schema:
                if prop.name == child:
                    return [nodes.paragraph('', nodes.Text(prop.description)), self.table(prop)]
            else:
                raise KeyError
        else:
            return [self.table(schema)]

    def row(self, prop, tbody):
        # Don't display rows for objects and arrays of objects (only their children)
        if (
            isinstance(prop, sphinxcontrib.jsonschema.Object)
            or (isinstance(prop, sphinxcontrib.jsonschema.Array) and prop.items.get('type') == 'object')
        ):
            return
        if not prop.rollup and prop.parent.parent.name != self.options.get('child'):
            return
        row = nodes.row()
        row += self.cell(prop.full_title)
        row += self.cell(prop.description or '')
        row += self.cell(type_format_simple(prop))
        row += self.cell(prop.required)
        tbody += row


class JSONSchemaTitleFieldnameMapDirective(sphinxcontrib.jsonschema.JSONSchemaDirective):
    headers = ['Title', 'Name', 'Type']
    widths = [1, 1, 1]

    def row(self, prop, tbody):
        # Don't display rows for objects and arrays of objects (only their children)
        if (isinstance(prop, sphinxcontrib.jsonschema.Object) or
            (isinstance(prop, sphinxcontrib.jsonschema.Array) and
                prop.items.get('type') == 'object')):
            return
        row = nodes.row()
        row += self.cell(prop.full_title)
        row += self.cell(prop.name)
        row += self.cell(type_format_simple(prop))
        tbody += row


class JSONSchemaArrayDirective(sphinxcontrib.jsonschema.JSONSchemaDirective):
    headers = ['', 'Description', 'Type', 'Required']
    widths = [1, 10, 2, 2]

    def row(self, prop, tbody):
        # Don't display rows for arrays and objects (only their children)
        if isinstance(prop, (sphinxcontrib.jsonschema.Array, sphinxcontrib.jsonschema.Object)):
            return

        assert prop.name.startswith('/0/')
        name = prop.name[3:]
        name_cell = nodes.entry('', nodes.literal('', nodes.Text(name)), morecols=3)

        row = nodes.row()
        row += name_cell
        tbody += row

        row = nodes.row()
        row += self.cell('')
        row += self.cell(prop.description or '')
        row += self.cell(type_format_simple(prop))
        row += self.cell(prop.required)
        tbody += row


class note(nodes.note, addnodes.translatable):
    ''' Named note as it needs to be a name that the sphinx builders know '''

    def preserve_original_messages(self):
        self['original_text'] = self.rawsource

    def apply_translated_message(self, original_message, translated_message):
        self.attributes['translation-found'] = True
        if translated_message.strip() == '-':
            self.attributes['ignore-note'] = True
        else:
            self.children = parse_markdown(translated_message)

    def extract_original_messages(self):
        return [self['original_text']]


class LocalizationNote(Note):

    def run(self):
        set_classes(self.options)
        self.assert_has_content()
        text = '\n'.join(self.content)
        self.options['localization_note'] = True
        admonition_node = note(text, **self.options)
        self.add_name(admonition_node)
        admonition_node.source, admonition_node.line = self.state.state_machine.get_source_and_line()
        # self.state.nested_parse(self.content, self.content_offset,
        #                         admonition_node)
        admonition_node.children = parse_markdown(text)
        return [admonition_node]


class RemoveLocalizationNote(Transform):
    """
    Remove localization note with a '-'.
    """
    default_priority = 21

    def apply(self):
        env = self.document.settings.env
        builder = env.app.builder
        if isinstance(builder, MessageCatalogBuilder):
            return
        for note in self.document.traverse(nodes.note):
            if 'localization_note' not in note.attributes:
                continue
            if (
                'ignore-note' in note.attributes or
                'translation-found' not in note.attributes or
                not env.config.language
            ):
                note.parent.remove(note)


def setup(app):
    app.add_directive('csv-table-no-translate', CSVTableNoTranslate)
    app.add_directive('directory_list', DirectoryListDirective)
    app.add_directive('jsoninclude', JSONInclude)
    app.add_directive('jsoninclude-flat', JSONIncludeFlat)
    app.add_directive('jsoninclude-quote', JSONIncludeQuote)
    app.add_directive('markdown', MarkdownDirective)
    app.add_directive('literal-and-parsed-markdown', LiteralAndParsedMarkdownDirective)
    app.add_directive('jsonschema-titles', JSONSchemaTitlesDirective)
    app.add_directive('jsonschema-title-fieldname-map', JSONSchemaTitleFieldnameMapDirective)
    app.add_directive('jsonschema-array', JSONSchemaArrayDirective)
    app.add_directive('localization-note', LocalizationNote)

    app.add_transform(RemoveLocalizationNote)
