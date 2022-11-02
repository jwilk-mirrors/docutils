#!/usr/bin/env python3

# $Id$
# Authors: Garth Kidd <garth@deadlybloodyserious.com>;
#          David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
The ``quicktest.py`` tool is used for testing the reStructuredText
parser.  It does not use a Docutils Reader or Writer or the standard
Docutils command-line options.  Rather, it does its own I/O and calls
the parser directly.  No transforms are applied to the parsed
document.  Possible output forms output include:

--pretty  Pretty-printed pseudo-XML (default)

--test    Test data (Python list of input and pseudo-XML output strings;
          useful for creating new test cases)
--xml     Pretty-printed native XML
--rawxml  Raw native XML (with or without a stylesheet reference)
--help    Usage hint and complete list of supported options.

.. Caution:: ``quicktest.py`` uses Python's default encoding.
   Input and output encoding depend on UTF-8 mode,
   Python version, locale setting, and operating system
   (cf. :PEP:`540`, :PEP:`538`, :PEP:`597`, and :PEP:`686`).
"""

try:
    import locale
    locale.setlocale(locale.LC_ALL, '')
except Exception:
    pass

import sys
import getopt
import docutils
from docutils import frontend
from docutils.utils import new_document
from docutils.parsers.rst import Parser


usage_header = """\
quicktest.py: Quickly test the reStructuredText parser.  This is not an
interface to the full functionality of Docutils.  Use one of the ``rst2*.py``
front-end tools instead.

Usage::

    quicktest.py [options] [<source> [<destination>]]

``source`` is the name of the file to use as input (default is stdin).
``destination`` is the name of the file to create as output (default is
stdout).

Options:
"""

options = [('pretty', 'p',
            'output pretty pseudo-xml: no "&abc;" entities (default)'),
           ('test', 't', 'output test-ready data (input & expected output, '
            'ready to be copied to a parser test module)'),
           ('rawxml', 'r', 'output raw XML'),
           ('styledxml=', 's', 'output raw XML with XSL style sheet '
            'reference (filename supplied in the option argument)'),
           ('xml', 'x', 'output pretty XML (indented)'),
           ('attributes', 'A', 'dump document attributes after processing'),
           ('debug', 'd', 'debug mode (lots of output)'),
           ('version', 'V', 'show Docutils version then exit'),
           ('help', 'h', 'show help text then exit')]
"""See ``distutils.fancy_getopt.FancyGetopt.__init__`` for a description of
the data structure: (long option, short option, description)."""


def usage():
    print(usage_header)
    for longopt, shortopt, description in options:
        if longopt[-1:] == '=':
            opts = '-%s arg, --%sarg' % (shortopt, longopt)
        else:
            opts = '-%s, --%s' % (shortopt, longopt)
        sys.stdout.write('%-15s' % opts)
        if len(opts) > 14:
            sys.stdout.write('%-16s' % '\n')
        while len(description) > 60:
            limit = description.rindex(' ', 0, 60)
            print(description[:limit].strip())
            description = description[limit + 1:]
            sys.stdout.write('%-15s' % ' ')
        print(description)


def _pretty(input, document, optargs):
    return document.pformat()


def _rawxml(input, document, optargs):
    return document.asdom().toxml()


def _styledxml(input, document, optargs):
    docnode = document.asdom().childNodes[0]
    return '\n'.join(('<?xml version="1.0" encoding="ISO-8859-1"?>',
                      '<?xml-stylesheet type="text/xsl" href="%s"?>'
                      % optargs['styledxml'],
                      docnode.toxml()))


def _prettyxml(input, document, optargs):
    return document.asdom().toprettyxml('    ', '\n')


def _test(input, document, optargs):
    tq = '"""'
    output = document.pformat()         # same as _pretty()
    return """\
    totest['change_this_test_name'] = [
[%s\\
%s
%s,
%s\\
%s
%s],
]
""" % (tq, escape(input.rstrip()), tq, tq, escape(output.rstrip()), tq)


def escape(text):
    """
    Return `text` in triple-double-quoted Python string form.
    """
    text = text.replace('\\', '\\\\')       # escape backslashes
    text = text.replace('"""', '""\\"')     # break up triple-double-quotes
    text = text.replace(' \n', ' \\n\\\n')  # protect trailing whitespace
    return text


_outputFormatters = {
    'rawxml': _rawxml,
    'styledxml': _styledxml,
    'xml': _prettyxml,
    'pretty': _pretty,
    'test': _test}


def format(outputFormat, input, document, optargs):
    formatter = _outputFormatters[outputFormat]
    return formatter(input, document, optargs)


def posixGetArgs(argv):
    outputFormat = 'pretty'
    # convert fancy_getopt style option list to getopt.getopt() arguments
    shortopts = ''.join(option[1] + ':' * (option[0][-1:] == '=')
                        for option in options if option[1])
    longopts = [option[0] for option in options if option[0]]
    try:
        opts, args = getopt.getopt(argv, shortopts, longopts)
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    optargs = {'debug': 0, 'attributes': 0}
    for o, a in opts:
        if o in ['-h', '--help']:
            usage()
            sys.exit()
        elif o in ['-V', '--version']:
            sys.stderr.write('quicktest.py (Docutils %s%s)\n' %
                             (docutils.__version__,
                              docutils.__version_details__
                              and ' [%s]'%docutils.__version_details__ or ''))
            sys.exit()
        elif o in ['-r', '--rawxml']:
            outputFormat = 'rawxml'
        elif o in ['-s', '--styledxml']:
            outputFormat = 'styledxml'
            optargs['styledxml'] = a
        elif o in ['-x', '--xml']:
            outputFormat = 'xml'
        elif o in ['-p', '--pretty']:
            outputFormat = 'pretty'
        elif o in ['-t', '--test']:
            outputFormat = 'test'
        elif o in ['--attributes', '-A']:
            optargs['attributes'] = 1
        elif o in ['-d', '--debug']:
            optargs['debug'] = 1
        else:
            raise getopt.GetoptError("getopt should have saved us!")
    if len(args) > 2:
        print('Maximum 2 arguments allowed.')
        usage()
        sys.exit(1)
    inputFile = sys.stdin
    outputFile = sys.stdout
    if args:
        inputFile = open(args.pop(0))
    if args:
        outputFile = open(args.pop(0), 'w')
    return inputFile, outputFile, outputFormat, optargs


def main():
    # process cmdline arguments:
    inputFile, outputFile, outputFormat, optargs = posixGetArgs(sys.argv[1:])
    settings = frontend.get_default_settings(Parser)
    settings.debug = optargs['debug']
    parser = Parser()
    input = inputFile.read()
    document = new_document(inputFile.name, settings)
    parser.parse(input, document)
    output = format(outputFormat, input, document, optargs)
    outputFile.write(output)
    if optargs['attributes']:
        import pprint
        pprint.pprint(document.__dict__)


if __name__ == '__main__':
    sys.stderr = sys.stdout
    main()
