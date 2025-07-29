import logging

import grokcore.component as grok
import zope.error.interfaces


@grok.implementer(zope.error.interfaces.IErrorReportingUtility)
class LoggingErrorReporting:
    grok.provides(zope.error.interfaces.IErrorReportingUtility)

    def __init__(
            self,
            info_level_errors=None,
            warning_level_errors=None,
            always_exc_info=False):
        self.logger = logging.getLogger('grokcore.error')
        self.info_level_errors = info_level_errors
        self.warning_level_errors = warning_level_errors
        self.always_exc_info = always_exc_info

    def make_extra(self, request=None):
        return None

    def raising(self, exc_info, request=None):
        exc_class = exc_info[0]
        msg = f'{exc_info[0].__name__} {str(exc_info[1])}'
        if request is not None:
            url = getattr(request, 'URL', None)
            if url is not None:
                msg += (' (URL: %s)' % url)

        level = self.logger.error

        if self.info_level_errors and \
                issubclass(exc_class, self.info_level_errors):
            level = self.logger.info
            exc_info = exc_info if self.always_exc_info else None

        elif self.warning_level_errors and \
                issubclass(exc_class, self.warning_level_errors):
            level = self.logger.warning
            exc_info = exc_info if self.always_exc_info else None

        try:
            level(msg, exc_info=exc_info, extra=self.make_extra(request))
        finally:
            exc_info = None  # gc cleanup.
