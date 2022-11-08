#!/usr/bin/env python3

# $Id$
# Author: Lea Wiemann <LeWiemann@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
Test for pseudo-XML writer.
"""

import unittest

from test import DocutilsTestSupport  # NoQA: F401

from docutils.core import publish_string


class WriterPublishTestCase(unittest.TestCase):
    maxDiff = None

    def test_publish(self):
        writer_name = 'pseudoxml'

        for name, cases in totest.items():
            for casenum, (case_input, case_expected) in enumerate(cases):
                with self.subTest(id=f'totest[{name!r}][{casenum}]'):
                    output = publish_string(
                        source=case_input,
                        writer_name=writer_name,
                        settings_overrides={
                            '_disable_config': True,
                            'strict_visitor': True,
                        },
                    )
                    if isinstance(output, bytes):
                        output = output.decode('utf-8')
                    self.assertEqual(output, case_expected)

        for name, cases in totest_detailed.items():
            for casenum, (case_input, case_expected) in enumerate(cases):
                with self.subTest(id=f'totest_detailed[{name!r}][{casenum}]'):
                    output = publish_string(
                        source=case_input,
                        writer_name=writer_name,
                        settings_overrides={
                            '_disable_config': True,
                            'strict_visitor': True,
                            'detailed': True,
                        },
                    )
                    if isinstance(output, bytes):
                        output = output.decode('utf-8')
                    self.assertEqual(output, case_expected)


totest = {}
totest_detailed = {}

totest['basic'] = [
# input
[r"""
This is a paragraph.

----------

This is a paragraph
with \escaped \characters.

A Section
---------

Foo.
""",
# output
"""\
<document source="<string>">
    <paragraph>
        This is a paragraph.
    <transition>
    <paragraph>
        This is a paragraph
        with escaped characters.
    <section ids="a-section" names="a\\ section">
        <title>
            A Section
        <paragraph>
            Foo.
"""]
]

totest_detailed['basic'] = [
# input
[totest['basic'][0][0],
# output
"""\
<document source="<string>">
    <paragraph>
        <#text>
            'This is a paragraph.'
    <transition>
    <paragraph>
        <#text>
            'This is a paragraph\\n'
            'with \\x00escaped \\x00characters.'
    <section ids="a-section" names="a\\ section">
        <title>
            <#text>
                'A Section'
        <paragraph>
            <#text>
                'Foo.'
"""]
]

if __name__ == '__main__':
    import unittest
    unittest.main()
