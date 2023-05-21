import requests
from django.http import JsonResponse
from django.views import View

url = "https://api.codelife.cc/api/top/list"


class NewsView(View):
    def post(self, request):

        headers = request.headers
        try:
            res = requests.post(url, data=request.data, headers={
                "signaturekey": headers['Signaturekey'],
                "version": '1.2.34',
            })
        except Exception:
            res = {'code': 501, 'msg': '请求错误', 'data': []}
        return JsonResponse(res.json())
