#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for the "sidebar" directive.
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

totest['sidebars'] = [
["""\
.. sidebar:: Outer

   .. sidebar:: Nested

      Body.
""",
"""\
<document source="test data">
    <sidebar>
        <title>
            Outer
        <system_message level="3" line="3" source="test data" type="ERROR">
            <paragraph>
                The "sidebar" directive may not be used within a sidebar element.
            <literal_block xml:space="preserve">
                .. sidebar:: Nested
                \n\
                   Body.
"""],
["""\
.. sidebar:: Margin Notes
   :subtitle: with options
   :class: margin
   :name: note:Options

   Body.
""",
"""\
<document source="test data">
    <sidebar classes="margin" ids="note-options" names="note:options">
        <title>
            Margin Notes
        <subtitle>
            with options
        <paragraph>
            Body.
"""],
["""\
.. sidebar::

   The title is optional.
""",
"""\
<document source="test data">
    <sidebar>
        <paragraph>
            The title is optional.
"""],
["""\
.. sidebar:: Outer

   .. topic:: Topic

      .. sidebar:: Inner

         text
""",
"""\
<document source="test data">
    <sidebar>
        <title>
            Outer
        <topic>
            <title>
                Topic
            <system_message level="3" line="5" source="test data" type="ERROR">
                <paragraph>
                    The "sidebar" directive may not be used within topics or body elements.
                <literal_block xml:space="preserve">
                    .. sidebar:: Inner
                    \n\
                       text
"""],
]


if __name__ == '__main__':
    import unittest
    unittest.main()
