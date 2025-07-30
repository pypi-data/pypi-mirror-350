import re
import sys

import lxml.html
import myst_parser
import pytest

from tests import path


def normalize(string):
    # Remove all newlines and indentation to normalise
    string = re.sub(r"\n *", "", string)
    # Remove <div class="clearer"></div> - some versions add this in and some don't,
    # so we need to normalise to one to make our test work with all versions
    string = string.replace('<div class="clearer"></div>', "")
    # but then add some
    # newlines back in to make pytest comparison output easier to read.
    string = string.replace(">", ">\n")
    return string


def assert_build(app, status, warning, basename, buildername='html', messages=None):
    app.build()
    warnings = warning.getvalue().strip()

    if buildername == 'html':
        with open(path(basename, '_build', buildername, 'index.html'), encoding='utf-8') as f:
            element = lxml.html.fromstring(f.read()).xpath('//div[@class="documentwrapper"]')[0]
            actual = lxml.html.tostring(element).decode()
            # This is only required for python 3.7 support
            if sys.version_info < (3, 8) or list(map(int, myst_parser.__version__.split("."))) < [0, 18, 0]:
                actual = re.sub(r'<colgroup>.*</colgroup>', '', actual, flags=re.DOTALL)

        with open(path(f'{basename}.html'), encoding='utf-8') as f:
            expected = f.read()

        assert normalize(actual) == normalize(expected)
    elif buildername == 'gettext':
        with open(path(basename, '_build', buildername, 'index.pot'), encoding='utf-8') as f:
            actual = re.sub(r"POT-Creation-Date: [0-9: +-]+", "POT-Creation-Date: ", f.read())

        with open(path(f'{basename}.pot'), encoding='utf-8') as f:
            expected = f.read()

        assert actual == expected

    assert 'build succeeded' in status.getvalue()

    if messages:
        for message in messages:
            assert message in warnings
        assert len(messages) == len(warnings.split('\n'))
    else:
        assert warnings == ''


@pytest.mark.sphinx(buildername='html', srcdir=path('csv-table-no-translate'), freshenv=True)
def test_csv_table_no_translate_html(app, status, warning):
    assert_build(app, status, warning, 'csv-table-no-translate')


@pytest.mark.sphinx(buildername='gettext', srcdir=path('csv-table-no-translate'), freshenv=True)
def test_csv_table_no_translate_gettext(app, status, warning):
    assert_build(app, status, warning, 'csv-table-no-translate', buildername='gettext')


@pytest.mark.sphinx(buildername='html', srcdir=path('csv-table-no-translate-md'), freshenv=True)
def test_csv_table_no_translate_html_myst(app, status, warning):
    assert_build(app, status, warning, 'csv-table-no-translate-md', buildername='html')


@pytest.mark.sphinx(buildername='gettext', srcdir=path('csv-table-no-translate-md'), freshenv=True)
def test_csv_table_no_translate_gettext_myst(app, status, warning):
    assert_build(app, status, warning, 'csv-table-no-translate-md', buildername='gettext')


@pytest.mark.sphinx(buildername='html', srcdir=path('jsoninclude-flat'), freshenv=True)
def test_jsoninclude_flat_html(app, status, warning):
    assert_build(app, status, warning, 'jsoninclude-flat')


@pytest.mark.sphinx(buildername='gettext', srcdir=path('jsoninclude-flat'), freshenv=True)
def test_jsoninclude_flat_gettext(app, status, warning):
    assert_build(app, status, warning, 'jsoninclude-flat', buildername='gettext')


@pytest.mark.sphinx(buildername='gettext', srcdir=path('jsoninclude-flat-md'), freshenv=True)
def test_jsoninclude_flat_gettext_myst(app, status, warning):
    assert_build(app, status, warning, 'jsoninclude-flat-md', buildername='gettext')


@pytest.mark.sphinx(buildername='html', srcdir=path('jsoninclude-quote'), freshenv=True)
def test_jsoninclude_quote_html(app, status, warning):
    assert_build(app, status, warning, 'jsoninclude-quote')
