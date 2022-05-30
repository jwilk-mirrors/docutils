# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Dummy module for backwards compatibility.

This module is provisional: it will be removed in Docutils 2.0.
"""

__docformat__ = 'reStructuredText'

import warnings

from docutils.parsers.rst.directives.misc import MetaBody, Meta  # noqa: F401

warnings.warn('The `docutils.parsers.rst.directive.html` module'
              ' will be removed in Docutils 2.0.'
              ' Since Docutils 0.18, the "Meta" node is defined in'
              ' `docutils.parsers.rst.directives.misc`.',
              DeprecationWarning, stacklevel=2)
