# from django.http import QueryDict
# from django.utils.deprecation import MiddlewareMixin

# class HttpPostTunnelingMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         if 'HTTP_X_METHODOVERRIDE' in request.META:
#             http_method = request.META['HTTP_X_METHODOVERRIDE']
#             if http_method.lower() == 'put':
#                 request.method  = 'PUT'
#                 request.META['REQUEST_METHOD'] = 'PUT'
#                 request.PUT = QueryDict(request.body)
#             if http_method.lower() == 'delete':
#                 request.method  = 'DELETE'
#                 request.META['REQUEST_METHOD'] = 'DELETE'
#                 request.DELETE = QueryDict(request.body)
#         return None 