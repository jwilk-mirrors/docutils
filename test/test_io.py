#! /usr/bin/env python3

# $Id$
# Author: Lea Wiemann <LeWiemann@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
Test module for `docutils.io`.
"""

import codecs
import locale
from io import StringIO, BytesIO
import os.path
from pathlib import Path
import sys
import unittest

if __name__ == '__main__':
    # prepend the "docutils root" to the Python library path
    # so we import the local `docutils` package.
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from docutils import io as du_io

# DATA_ROOT is ./test/data/ from the docutils root
DATA_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')

# normalize the preferred encoding's name:
preferredencoding = codecs.lookup(
    locale.getpreferredencoding(do_setlocale=False)).name


# Stub: Buffer with 'strict' auto-conversion of input to byte string:
class BBuf(BytesIO):
    def write(self, data):
        if isinstance(data, str):
            data.encode('ascii', 'strict')
        super().write(data)


# Stub: Buffer expecting unicode string:
class UBuf(StringIO):
    def write(self, data):
        # emulate Python 3 handling of stdout, stderr
        if isinstance(data, bytes):
            raise TypeError('must be unicode, not bytes')
        super().write(data)


class mock_stdout(UBuf):
    encoding = 'utf-8'

    def __init__(self):
        self.buffer = BBuf()
        super().__init__()


class HelperTests(unittest.TestCase):

    def test_check_encoding_true(self):
        """Return `True` if lookup returns the same codec"""
        self.assertEqual(du_io.check_encoding(mock_stdout, 'utf-8'), True)
        self.assertEqual(du_io.check_encoding(mock_stdout, 'utf_8'), True)
        self.assertEqual(du_io.check_encoding(mock_stdout, 'utf8'), True)
        self.assertEqual(du_io.check_encoding(mock_stdout, 'UTF-8'), True)

    def test_check_encoding_false(self):
        """Return `False` if lookup returns different codecs"""
        self.assertEqual(du_io.check_encoding(mock_stdout, 'ascii'), False)
        self.assertEqual(du_io.check_encoding(mock_stdout, 'latin-1'), False)

    def test_check_encoding_none(self):
        """Cases where the comparison fails."""
        # stream.encoding is None:
        self.assertEqual(du_io.check_encoding(du_io.FileInput(), 'ascii'),
                         None)
        # stream.encoding does not exist:
        self.assertEqual(du_io.check_encoding(BBuf, 'ascii'), None)
        # encoding is None or empty string:
        self.assertEqual(du_io.check_encoding(mock_stdout, None), None)
        self.assertEqual(du_io.check_encoding(mock_stdout, ''), None)
        # encoding is invalid
        self.assertEqual(du_io.check_encoding(mock_stdout, 'UTF-9'), None)

    def test_error_string(self):
        us = '\xfc'       # bytes(us) fails
        bs = b'\xc3\xbc'  # str(bs) returns repr(bs)

        self.assertEqual('Exception: spam',
                         du_io.error_string(Exception('spam')))
        self.assertEqual('IndexError: ' + str(bs),
                         du_io.error_string(IndexError(bs)))
        self.assertEqual('ImportError: %s' % us,
                         du_io.error_string(ImportError(us)))


class InputTests(unittest.TestCase):

    def test_bom_handling(self):
        # Provisional:
        # default input encoding will change to UTF-8 in Docutils 0.22
        source = '\ufeffdata\n\ufeff blah\n'
        expected = 'data\n\ufeff blah\n'  # only leading ZWNBSP removed
        input = du_io.StringInput(source=source.encode('utf-16-be'))
        self.assertEqual(input.read(), expected)
        input = du_io.StringInput(source=source.encode('utf-16-le'))
        self.assertEqual(input.read(), expected)
        input = du_io.StringInput(source=source.encode('utf-8'))
        self.assertEqual(input.read(), expected)
        # With `str` input all ZWNBSPs are still there.
        input = du_io.StringInput(source=source)
        self.assertEqual(input.read(), source)

    def test_encoding_declaration(self):
        input = du_io.StringInput(source=b"""\
.. -*- coding: ascii -*-
data
blah
""")
        data = input.read()  # noqa: F841
        self.assertEqual(input.successful_encoding, 'ascii')
        input = du_io.StringInput(source=b"""\
#! python
# -*- coding: ascii -*-
print("hello world")
""")
        data = input.read()  # noqa: F841
        self.assertEqual(input.successful_encoding, 'ascii')
        input = du_io.StringInput(source=b"""\
#! python
# extraneous comment; prevents coding slug from being read
# -*- coding: ascii -*-
print("hello world")
""")
        self.assertNotEqual(input.successful_encoding, 'ascii')

    def test_decode_unicode(self):
        # With the special value "unicode" or "Unicode":
        uniinput = du_io.Input(encoding='unicode')
        # keep unicode instances as-is
        self.assertEqual(uniinput.decode('ja'), 'ja')
        # raise AssertionError if data is not a `str` instance
        with self.assertRaises(AssertionError):
            uniinput.decode(b'ja')


class OutputTests(unittest.TestCase):

    bdata = b'\xfc'
    udata = '\xfc'

    def setUp(self):
        self.bdrain = BBuf()
        """Buffer accepting binary strings (bytes)"""
        self.udrain = UBuf()
        """Buffer accepting unicode strings"""
        self.mock_stdout = mock_stdout()
        """Stub of sys.stdout under Python 3"""

    def test_write_unicode(self):
        fo = du_io.FileOutput(destination=self.udrain, encoding='unicode',
                              autoclose=False)
        fo.write(self.udata)
        self.assertEqual(self.udrain.getvalue(), self.udata)

    def test_write_utf8(self):
        fo = du_io.FileOutput(destination=self.udrain, encoding='utf-8',
                              autoclose=False)
        fo.write(self.udata)
        self.assertEqual(self.udrain.getvalue(), self.udata)

    def test_FileOutput_hande_io_errors_deprection_warning(self):
        with self.assertWarnsRegex(DeprecationWarning,
                                   '"handle_io_errors" is ignored'):
            du_io.FileOutput(handle_io_errors=True)

    # With destination in binary mode, data must be binary string
    # and is written as-is:
    def test_write_bytes(self):
        fo = du_io.FileOutput(destination=self.bdrain, encoding='utf-8',
                              mode='wb', autoclose=False)
        fo.write(self.bdata)
        self.assertEqual(self.bdrain.getvalue(), self.bdata)

    def test_write_bytes_to_stdout(self):
        # try writing data to `destination.buffer`, if data is
        # instance of `bytes` and writing to `destination` fails:
        fo = du_io.FileOutput(destination=self.mock_stdout)
        fo.write(self.bdata)
        self.assertEqual(self.mock_stdout.buffer.getvalue(),
                         self.bdata)

    def test_encoding_clash_resolved(self):
        fo = du_io.FileOutput(destination=self.mock_stdout,
                              encoding='latin1', autoclose=False)
        fo.write(self.udata)
        self.assertEqual(self.mock_stdout.buffer.getvalue(),
                         self.udata.encode('latin1'))

    def test_encoding_clash_nonresolvable(self):
        del self.mock_stdout.buffer
        fo = du_io.FileOutput(destination=self.mock_stdout,
                              encoding='latin1', autoclose=False)
        self.assertRaises(ValueError, fo.write, self.udata)


class ErrorOutputTests(unittest.TestCase):
    def test_defaults(self):
        e = du_io.ErrorOutput()
        self.assertEqual(e.destination, sys.stderr)

    def test_bbuf(self):
        buf = BBuf()  # buffer storing byte string
        e = du_io.ErrorOutput(buf, encoding='ascii')
        # write byte-string as-is
        e.write(b'b\xfc')
        self.assertEqual(buf.getvalue(), b'b\xfc')
        # encode unicode data with backslashescape fallback replacement:
        e.write(' u\xfc')
        self.assertEqual(buf.getvalue(), b'b\xfc u\\xfc')
        # handle Exceptions with Unicode string args
        # unicode(Exception('e\xfc')) # fails in Python < 2.6
        e.write(AttributeError(' e\xfc'))
        self.assertEqual(buf.getvalue(), b'b\xfc u\\xfc e\\xfc')
        # encode with `encoding` attribute
        e.encoding = 'utf-8'
        e.write(' u\xfc')
        self.assertEqual(buf.getvalue(), b'b\xfc u\\xfc e\\xfc u\xc3\xbc')

    def test_ubuf(self):
        buf = UBuf()  # buffer only accepting unicode string
        # decode of binary strings
        e = du_io.ErrorOutput(buf, encoding='ascii')
        e.write(b'b\xfc')
        # use REPLACEMENT CHARACTER
        self.assertEqual(buf.getvalue(), 'b\ufffd')
        # write Unicode string and Exceptions with Unicode args
        e.write(' u\xfc')
        self.assertEqual(buf.getvalue(), 'b\ufffd u\xfc')
        e.write(AttributeError(' e\xfc'))
        self.assertEqual(buf.getvalue(), 'b\ufffd u\xfc e\xfc')
        # decode with `encoding` attribute
        e.encoding = 'latin1'
        e.write(b' b\xfc')
        self.assertEqual(buf.getvalue(), 'b\ufffd u\xfc e\xfc b\xfc')


class FileInputTests(unittest.TestCase):

    # test input encoding auto-detection:
    #
    # Up to Docutils 0.18, auto-detection was not used under Python 3
    # unless reading a file with Python's default encoding failed

    def test_bom_utf_8(self):
        """Drop optional BOM from utf-8 encoded files.
        """
        source = du_io.FileInput(
            source_path=os.path.join(DATA_ROOT, 'utf-8-sig.txt'))
        self.assertTrue(source.read().startswith('Grüße'))

    def test_bom_utf_16(self):
        """Drop BOM from utf-16 encoded files, use correct encoding.
        """
        # Assert correct decoding, BOM is gone.
        source = du_io.FileInput(
            source_path=os.path.join(DATA_ROOT, 'utf-16-le-sig.txt'))
        self.assertTrue(source.read().startswith('Grüße'))

    def test_coding_slug(self):
        """Use self-declared encoding.
        """
        source = du_io.FileInput(
            source_path=os.path.join(DATA_ROOT, 'latin2.txt'))
        self.assertTrue(source.read().endswith('škoda\n'))

    def test_fallback_utf8(self):
        """Try 'utf-8', if encoding is not specified in the source."""
        source = du_io.FileInput(
            source_path=os.path.join(DATA_ROOT, 'utf8.txt'))
        self.assertEqual(source.read(), 'Grüße\n')

    @unittest.skipIf(preferredencoding in (None, 'ascii', 'utf-8'),
                     'locale encoding not set or UTF-8')
    def test_fallback_no_utf8(self):
        # If  no encoding is given and decoding with 'utf-8' fails,
        # use the locale's preferred encoding (if not None).
        # Provisional: the default will become 'utf-8'
        # (without auto-detection and fallback) in Docutils 0.22.
        source = du_io.FileInput(
            source_path=os.path.join(DATA_ROOT, 'latin1.txt'))
        data = source.read()
        successful_encoding = codecs.lookup(source.successful_encoding).name
        self.assertEqual(successful_encoding, preferredencoding)
        if successful_encoding == 'iso8859-1':
            self.assertEqual(data, 'Grüße\n')

    def test_readlines(self):
        source = du_io.FileInput(
            source_path=os.path.join(DATA_ROOT, 'include.txt'))
        data = source.readlines()
        self.assertEqual(data, ['Some include text.\n'])


if __name__ == '__main__':
    unittest.main()
