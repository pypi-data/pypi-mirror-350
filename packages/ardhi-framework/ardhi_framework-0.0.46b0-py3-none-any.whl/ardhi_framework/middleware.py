import threading

_request_local = threading.local()


def get_current_request():
    return getattr(_request_local, 'request', None)


class RequestFetchMiddleware:
    """
    Middleware that stores the request in thread local storage.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _request_local.request = request
        response = self.get_response(request)
        return response


class DefaultLoggerMiddleware:
    def __init__(self, logger):
        self.logger = logger




