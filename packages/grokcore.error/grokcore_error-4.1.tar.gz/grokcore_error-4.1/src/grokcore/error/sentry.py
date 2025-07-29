import zope.publisher.interfaces.http

import grokcore.error


_request_iface = zope.publisher.interfaces.http.IHTTPApplicationRequest


class SentryAwareLoggingErrorReporting(grokcore.error.LoggingErrorReporting):

    def make_extra(self, request=None):
        if request is None:
            return None
        if not _request_iface.providedBy(request):
            return None
        host = request.getHeader(
            'HTTP_X_FORWARDED_FOR',
            request.getHeader('REMOTE_ADDR'))
        # Only push the first 10K of bytes to sentry.
        data = request.bodyStream.getCacheStream().read(10 * 1024)

        environ = {}
        headers = {}
        for key, value in request._environ.items():
            if key.startswith('HTTP_'):
                headers[key[5:].replace('_', '-').capitalize()] = value
            else:
                environ[key] = value

        result = {
            'sentry.interfaces.Http': {
                'url': request.getURL(),
                'method': request.method,
                'headers': headers,
                'cookies': headers.get('Cookie'),
                'query_string': environ.get('QUERY_STRING'),
                'env': environ,
                'host': host,
                'data': data,
            }
        }

        if getattr(request, 'principal', None) is not None:
            result['sentry.interfaces.User'] = {
                'id': request.principal.id
            }

        return result
