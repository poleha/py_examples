"""
Creating request and response, applying middleware

1) Сначала вызывается class WSGIHandler(base.BaseHandler). Он получает dict environ
2)в нем создается class WSGIRequest(http.HttpRequest) request = self.request_class(environ)
3) and response response = self.get_response(request)
4) Вызывается BaseHandler.get_response(self, request), which iterates through middleware:
for middleware_method in self._request_middleware:
                response = middleware_method(request)
                if response:
                    break

if middleware returns response, it is passed to view function or class
in normal case it returns None

each middleware adds something to request, which is still WSGIRequest

5) We iterate through view middleware
for middleware_method in self._view_middleware:
                    response = middleware_method(request, callback, callback_args, callback_kwargs)
                    if response:
                        break
each middleware adds something to request, which is still WSGIRequest
in normal case it returns None

6) we're still in BaseHandler.get_response(self, request)

if response is None:
                wrapped_callback = self.make_view_atomic(callback)  - wrapped_callback - view class
                try:
                    response = wrapped_callback(request, *callback_args, **callback_kwargs)

where response - TemplateResponse
"""