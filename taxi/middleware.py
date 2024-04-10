# middleware.py

from django.utils.deprecation import MiddlewareMixin

class XFrameOptionsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['X-Frame-Options'] = 'ALLOW-FROM http://localhost:8000'
        return response
