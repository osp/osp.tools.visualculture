"""
Users of the API might have to deal with failed requests.
This middleware catches errors raised by urllib2’s urlopen,
and sends an HTTP error with the same return code to the
client, so that she or he knows what’s going on.
"""

from urllib2 import HTTPError
from django.http import Http404

class APIError(object):
    def process_exception(self, request, exception):
        if isinstance(exception, HTTPError):
            if exception.code == 404:
                raise Http404
            else:
                return HttpResponse(status=exception.code)
        else:
            return None