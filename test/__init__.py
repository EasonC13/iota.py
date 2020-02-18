# coding=utf-8
from __future__ import absolute_import, division, print_function, \
  unicode_literals

from six import PY3

if PY3:
  # In Python 3 the ``mock`` library was moved into the stdlib.
  # noinspection PyUnresolvedReferences
  from unittest import mock
  from unittest.mock import MagicMock, patch
else:
  # In Python 2, the ``mock`` library is included as a dependency.
  # noinspection PyUnresolvedReferences
  import mock
  from mock import MagicMock, patch

# Executes async test case within a loop
from aiounittest import async_test
