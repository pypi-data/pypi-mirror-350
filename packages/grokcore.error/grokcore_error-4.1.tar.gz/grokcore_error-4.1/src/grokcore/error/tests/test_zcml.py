import unittest
from unittest import mock

from grokcore.error.errorreport import LoggingErrorReporting
from grokcore.error.zcml import errorreportingutility


class ZcmlTestCase(unittest.TestCase):

    def test_errorreportingutility(self):
        _context = mock.Mock()
        errorreportingutility(_context, factory=LoggingErrorReporting)
        self.assertTrue(_context.action.called)
