#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for the target-notes directives.
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

totest['target_notes'] = [
["""\
.. target-notes::
""",
"""\
<document source="test data">
    <pending>
        .. internal attributes:
             .transform: docutils.transforms.references.TargetNotes
             .details:
"""],
["""\
.. target-notes:: :class: custom
""",
"""\
<document source="test data">
    <pending>
        .. internal attributes:
             .transform: docutils.transforms.references.TargetNotes
             .details:
               class: ['custom']
"""],
["""\
.. target-notes::
   :class: custom
   :name: targets
""",
"""\
<document source="test data">
    <pending ids="targets" names="targets">
        .. internal attributes:
             .transform: docutils.transforms.references.TargetNotes
             .details:
               class: ['custom']
"""],
["""\
.. target-notes::
   :class:
""",
"""\
<document source="test data">
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Error in "target-notes" directive:
            invalid option value: (option: "class"; value: None)
            argument required but none supplied.
        <literal_block xml:space="preserve">
            .. target-notes::
               :class:
"""],
]


if __name__ == '__main__':
    import unittest
    unittest.main()
