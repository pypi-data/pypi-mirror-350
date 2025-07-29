import doctest
import logging
import unittest

import zope.component.testlayer

import grokcore.error


class Layer(zope.component.testlayer.ZCMLFileLayer):
    pass


layer = Layer(grokcore.error, zcml_file='testing.zcml')


class Example:
    def __init__(self, expected):
        self.want = expected


class OutputCheckerMixin:

    def __init__(self, *arg, **kw):
        super().__init__(*arg, **kw)
        # In case *both* comparision items are strings
        self.addTypeEqualityFunc(str, self._check_basestring)

    def _check_basestring(self, expected, actual, msg=None):
        flags = (
            doctest.ELLIPSIS +
            doctest.NORMALIZE_WHITESPACE +
            doctest.REPORT_NDIFF)
        checker = doctest.OutputChecker()
        right = checker.check_output(expected, actual, flags)
        if not right:
            diff = checker.output_difference(Example(expected), actual, flags)
            raise self.failureException(diff)
        return right


class TestCase(OutputCheckerMixin, unittest.TestCase):
    pass


class Logger(logging.Handler):
    """
    This logging handler can be used for listening to emitted log records.

    This is useful when you want to explicitely follow log records emitted
    deep within another library.

    E.g. to follow log records emitted by the ``grokcore.error`` logging
    error reporting utilitym you can do the following::

        with Logger('grokcore.error') as log:
            # trigger log emitting code

        print log.records
    """

    def __init__(self, name=''):
        logging.Handler.__init__(self)
        self.name = name
        self._records = []
        self._level = 1
        self._levels = {}

    @property
    def records(self):
        return self._records

    def emit(self, record):
        self._records.append(record)

    def __enter__(self):
        logger = logging.getLogger(self.name)
        self._levels[self.name] = logger.level
        logger.setLevel(self._level)
        logger.addHandler(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger = logging.getLogger(self.name)
        logger.setLevel(self._levels[self.name])
        logger.removeHandler(self)
