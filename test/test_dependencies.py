#! /usr/bin/env python3

# $Id$
# Author: Lea Wiemann <LeWiemann@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
Test module for the --record-dependencies option.
"""

import os.path
import unittest
from io import StringIO

import docutils.core
import docutils.utils
import docutils.io
from docutils.parsers.rst.directives.images import PIL

# TEST_ROOT is ./test/ from the docutils root
TEST_ROOT = os.path.abspath(os.path.dirname(__file__))
# DATA_ROOT is ./test/data/ from the docutils root
DATA_ROOT = os.path.join(TEST_ROOT, 'data')


def relpath(*parts):
    return os.path.relpath(
        os.path.join(*parts), os.getcwd()).replace('\\', '/')


# docutils.utils.DependencyList records POSIX paths,
# i.e. "/" as a path separator even on Windows (not os.path.join).
paths = {
    'include': relpath(DATA_ROOT, 'include.txt'),  # included rst file
    'raw': relpath(DATA_ROOT, 'raw.txt'),      # included raw "HTML file"
    'scaled-image': relpath(TEST_ROOT,
                            '../docs/user/rst/images/biohazard.png'),
    'figure-image': relpath(TEST_ROOT, '../docs/user/rst/images/title.png'),
    'stylesheet': relpath(DATA_ROOT, 'stylesheet.txt'),
}

# avoid latex writer future warnings:
latex_settings_overwrites = {'legacy_column_widths': False,
                             'use_latex_citations': True}


class RecordDependenciesTests(unittest.TestCase):

    def get_record(self, **settings):
        recordfile = 'record.txt'
        recorder = docutils.utils.DependencyList(recordfile)
        # (Re) create the record file by running a conversion:
        settings.setdefault('source_path',
                            os.path.join(DATA_ROOT, 'dependencies.txt'))
        settings.setdefault('settings_overrides', {})
        settings['settings_overrides'].update(_disable_config=True,
                                              record_dependencies=recorder)
        docutils.core.publish_file(destination=StringIO(),  # ignored
                                   **settings)
        recorder.close()
        # Read the record file:
        with open(recordfile, encoding='utf-8') as record:
            return record.read().splitlines()

    def test_dependencies_xml(self):
        # Note: currently, raw input files are read (and hence recorded) while
        # parsing even if not used in the chosen output format.
        # This should change (see parsers/rst/directives/misc.py).
        keys = ['include', 'raw']
        if PIL:
            keys += ['figure-image']
        expected = [paths[key] for key in keys]
        record = sorted(self.get_record(writer_name='xml'))
        # the order of the files is arbitrary
        expected.sort()
        self.assertEqual(record, expected)

    def test_dependencies_html(self):
        keys = ['include', 'raw']
        if PIL:
            keys += ['figure-image', 'scaled-image']
        expected = [paths[key] for key in keys]
        # stylesheets are tested separately in test_stylesheet_dependencies():
        so = {'stylesheet_path': None, 'stylesheet': None}
        record = sorted(self.get_record(writer_name='html',
                                        settings_overrides=so))
        # the order of the files is arbitrary
        expected.sort()
        self.assertEqual(record, expected)

    def test_dependencies_latex(self):
        # since 0.9, the latex writer records only really accessed files, too.
        # Note: currently, raw input files are read (and hence recorded) while
        # parsing even if not used in the chosen output format.
        # This should change (see parsers/rst/directives/misc.py).
        keys = ['include', 'raw']
        if PIL:
            keys += ['figure-image']
        expected = [paths[key] for key in keys]
        record = sorted(self.get_record(
                            writer_name='latex',
                            settings_overrides=latex_settings_overwrites))
        # the order of the files is arbitrary
        expected.sort()
        self.assertEqual(record, expected)

    def test_csv_dependencies(self):
        csvsource = os.path.join(DATA_ROOT, 'csv_dep.txt')
        self.assertEqual(self.get_record(source_path=csvsource),
                         [relpath(DATA_ROOT, 'csv_data.txt')])

    def test_stylesheet_dependencies(self):
        stylesheet = paths['stylesheet']
        so = {'stylesheet_path': paths['stylesheet'],
              'stylesheet': None}
        so.update(latex_settings_overwrites)
        so['embed_stylesheet'] = False
        record = self.get_record(writer_name='html', settings_overrides=so)
        self.assertTrue(stylesheet not in record,
                        '%r should not be in %r' % (stylesheet, record))
        record = self.get_record(writer_name='latex', settings_overrides=so)
        self.assertTrue(stylesheet not in record,
                        '%r should not be in %r' % (stylesheet, record))

        so['embed_stylesheet'] = True
        record = self.get_record(writer_name='html', settings_overrides=so)
        self.assertTrue(stylesheet in record,
                        '%r should be in %r' % (stylesheet, record))
        so['embed_stylesheet'] = True
        record = self.get_record(writer_name='latex', settings_overrides=so)
        self.assertTrue(stylesheet in record,
                        '%r should be in %r' % (stylesheet, record))

    def tearDown(self) -> None:
        os.unlink("record.txt")


if __name__ == '__main__':
    unittest.main()
