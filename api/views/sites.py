from django.views import View
from django.http import JsonResponse
from app01.models import Navs, NavTags
from django import forms
from api.views.login import clean_form
import datetime


class NavTagsView(View):
    def post(self, request, **kwargs):
        res = {
            'msg': '标签添加成功',
            'code': 502,
            'self': None,
        }
        if not request.user.is_superuser:
            res['msg'] = '用户验证失败'
            return JsonResponse(res)

        title = request.data.get('title')
        if not title:
            res['msg'] = '请输入标签名'
            return JsonResponse(res)

        nid = kwargs.get('nid')
        if nid:
            # 编辑标签
            tag_query = NavTags.objects.filter(nid=nid)
            tag_query.update(title=title)
            res['msg'] = '标签编辑成功'
            res['code'] = 0
            return JsonResponse(res)

        tag_query = NavTags.objects.filter(title=title)
        if tag_query:
            res['msg'] = '该标签已存在'
            return JsonResponse(res)

        NavTags.objects.create(title=title)
        res['code'] = 0
        return JsonResponse(res)

    def delete(self, request, nid):
        res = {
            'msg': '删除标签成功',
            'code': 412,
        }
        if not request.user.is_superuser:
            res['msg'] = '用户验证失败'
            return JsonResponse(res)

        site_query = NavTags.objects.filter(nid=nid)
        if site_query:
            site_query.delete()
        res['code'] = 0
        return JsonResponse(res)


class NavView(View):
    def get(self, request):
        title = request.GET.get('title')
        data = []
        nav_list = Navs.objects.filter(tag__title=title, status=1)
        for nav in nav_list:
            data.append({
                'title': nav.title,
                'abstract': nav.abstract,
                'href': nav.href,
                'icon_href': nav.icon_href,
                'create_date': nav.create_date.strftime("%Y-%m-%d"),
                'collects_count': nav.collects_count,
                'digg_count': nav.digg_count,
                'tags': [tag.title for tag in nav.tag.all()],
            })

        print(data)
        return JsonResponse(data, safe=False)
