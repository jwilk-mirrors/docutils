#!/usr/bin/env python3
# :Copyright: © 2020 Günter Milde.
# :License: Released under the terms of the `2-Clause BSD license`_, in short:
#
#    Copying and distribution of this file, with or without modification,
#    are permitted in any medium without royalty provided the copyright
#    notice and this notice are preserved.
#    This file is offered as-is, without any warranty.
#
# .. _2-Clause BSD license: https://opensource.org/licenses/BSD-2-Clause

"""
Various tests for the recommonmark parser.
"""

import unittest

from docutils.core import publish_string
from docutils.parsers.rst import directives as rst_directives
from docutils.parsers.recommonmark_wrapper import Parser


sample_with_html = """\
A paragraph:

<p>A HTML block.</p>

Next paragraph.

<script type="text/javascript">
// some dangerous JavaScript

Final paragraph.
"""


class RecommonmarkParserTests(unittest.TestCase):

    def test_parser_name(self):
        # cf. ../test_rst/test_directives/test__init__.py
        # this is used in the "include" directive's :parser: option.
        self.assertIs(rst_directives.parser_name('recommonmark'), Parser)

    def test_raw_disabled(self):
        output = publish_string(sample_with_html, parser=Parser(),
                                settings_overrides={
                                    'warning_stream': '',
                                    'raw_enabled': False,
                                    'output_encoding': 'unicode',
                                })
        self.assertNotIn('<raw>', output)
        self.assertIn('<system_message', output)
        self.assertIn('Raw content disabled.', output)

    def test_raw_disabled_inline(self):
        output = publish_string('foo <a href="uri">', parser=Parser(),
                                settings_overrides={
                                    'warning_stream': '',
                                    'raw_enabled': False,
                                    'output_encoding': 'unicode',
                                })
        self.assertNotIn('<raw>', output)
        self.assertIn('<system_message', output)
        self.assertIn('Raw content disabled.', output)


if __name__ == '__main__':
    unittest.main()
