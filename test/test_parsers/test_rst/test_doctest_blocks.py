#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for states.py.
"""

import unittest

from test import DocutilsTestSupport  # NoQA: F401

from docutils.frontend import get_default_settings
from docutils.parsers.rst import Parser
from docutils.utils import new_document


class ParserTestCase(unittest.TestCase):
    def test_parser(self):
        parser = Parser()
        settings = get_default_settings(Parser)
        settings.warning_stream = ''
        for name, cases in totest.items():
            for casenum, (case_input, case_expected) in enumerate(cases):
                with self.subTest(id=f'totest[{name!r}][{casenum}]'):
                    document = new_document('test data', settings.copy())
                    parser.parse(case_input, document)
                    output = document.pformat()
                    self.assertEqual(output, case_expected)


totest = {}

totest['doctest_blocks'] = [
["""\
Paragraph.

>>> print("Doctest block.")
Doctest block.

Paragraph.
""",
"""\
<document source="test data">
    <paragraph>
        Paragraph.
    <doctest_block xml:space="preserve">
        >>> print("Doctest block.")
        Doctest block.
    <paragraph>
        Paragraph.
"""],
["""\
Paragraph.

>>> print("    Indented output.")
    Indented output.
""",
"""\
<document source="test data">
    <paragraph>
        Paragraph.
    <doctest_block xml:space="preserve">
        >>> print("    Indented output.")
            Indented output.
"""],
["""\
Paragraph.

    >>> print("    Indented block & output.")
        Indented block & output.
""",
"""\
<document source="test data">
    <paragraph>
        Paragraph.
    <block_quote>
        <doctest_block xml:space="preserve">
            >>> print("    Indented block & output.")
                Indented block & output.
"""],
]

if __name__ == '__main__':
    import unittest
    unittest.main()
