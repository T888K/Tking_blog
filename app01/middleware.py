from __future__ import unicode_literals

import json
from django.utils.deprecation import MiddlewareMixin


class MD1(MiddlewareMixin):
    # 请求中间件
    def process_request(self, request):
        if request.method != 'GET' and request.content_type == 'application/json':
            data = json.loads(request.body)
            request.data = data

    # 响应中间件
    def process_response(self, request, response):
        return response
