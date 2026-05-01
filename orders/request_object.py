from . import models

# def simple_middleware(get_response):
def RequestObjectMiddleware(get_response): #Just changed the function name.
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        models.request_object = request #assigning the request to request_object variable in models.py

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware