from django.views import View
from django.http import JsonResponse
from markdown import markdown
from pyquery import PyQuery
from app01.models import Tags, Articles, Cover
from django import forms
from api.views.login import clean_form
from django.db.models import F
import random


# 文章
# class ArticleView(View):
#     # 发布文章
#     def post(self, request):
#         res = {
#             'msg': '文章发布成功',
#             'code': 412,
#             'data': None
#         }
#         data: dict = request.data
#         title = data.get('title')
#         if not title:
#             res['msg'] = '请输入文章标题'
#             return JsonResponse(res)
#
#         author = data.get('author')
#         if not author:
#             res['msg'] = '请输入文章作者'
#             return JsonResponse(res)
#
#         source = data.get('source')
#         if not source:
#             res['msg'] = '请输入文章来源'
#             return JsonResponse(res)
#
#         content = data.get('content')
#         recommend = data.get('recommend')
#         if not content:
#             res['msg'] = '请输入文章内容'
#             return JsonResponse(res)
#         extra = {
#             'title': title,
#             'author': author,
#             'source': source,
#             'content': content,
#             'recommend': recommend,
#             'status': 1
#         }
#
#         abstract = data.get('abstract')
#         if not abstract:
#             abstract = PyQuery(markdown(content)).text()[:30]
#         extra['abstract'] = abstract
#
#         category = data.get('category_id')
#         if category:
#             extra['category'] = category
#
#         cover_id = data.get('cover_id')
#         if cover_id:
#             extra['cover_id'] = cover_id
#         else:
#             extra['cover_id'] = 1
#
#         pwd = data.get('pwd')
#         if pwd:
#             extra['pwd'] = pwd
#
#         # 添加文章
#         article_obj = Articles.objects.create(**extra)
#         # 标签 比较特殊
#         tags = data.get('tags')
#         if tags:
#             for tag in tags:
#                 if not tag.isdigit():
#                     tag_obj = Tags.objects.create(title=tag)
#                     article_obj.tag.add(tag_obj)
#                 else:
#                     article_obj.tag.add(tag)
#
#         res['code'] = 0
#         res['data'] = article_obj.nid
#         return JsonResponse(res)

class AddArticleForm(forms.Form):
    title = forms.CharField(error_messages={'required': '请输入文章标题'})
    author = forms.CharField(error_messages={'required': '请输入文章作者'})
    source = forms.CharField(error_messages={'required': '请输入文章来源'})
    content = forms.CharField(error_messages={'required': '请输入文章内容'})

    category = forms.IntegerField(required=False)
    pwd = forms.CharField(required=False)
    recommend = forms.BooleanField(required=False)
    status = forms.IntegerField(required=False)

    # 文章简介,文章封面不进行为空验证
    abstract = forms.CharField(required=False)
    cover_id = forms.IntegerField(required=False)

    word = forms.IntegerField(required=False)

    # 全局钩子
    def clean(self):
        category = self.cleaned_data['category']
        if not category:
            self.cleaned_data.pop('category')

        pwd = self.cleaned_data['pwd']
        if not pwd:
            self.cleaned_data.pop('pwd')

    # 文章简介局部钩子
    def clean_abstract(self):
        abstract = self.cleaned_data['abstract']
        if abstract:
            return abstract
        # 没有就去截取正文的30个字符
        content = self.cleaned_data.get('content')
        if content:
            abstract = PyQuery(markdown(content)).text()[:90]
            return abstract

    # 文章封面局部钩子
    def clean_cover_id(self):
        cover_id = self.cleaned_data["cover_id"]
        if cover_id:
            return cover_id
        cover_set = Cover.objects.all().values('nid')
        cover_id = random.choice(cover_set)['nid']
        return cover_id


# 给文章添加标签
def add_article_tags(tags, article_obj):
    for tag in tags:
        if tag.isdigit():
            # 数据库里面有的直接加进去
            article_obj.tag.add(tag)
        else:
            # 没有的就先创建在添加进去
            tag_obj = Tags.objects.create(title=tag)
            article_obj.tag.add(tag_obj.nid)


class ArticleView(View):
    # 添加文章
    def post(self, request):
        res = {
            'msg': '文章发布成功',
            'code': 412,
            'data': None
        }
        data = request.data
        data['status'] = 1
        form = AddArticleForm(data)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 校验通过
        article_obj = Articles.objects.create(**form.cleaned_data)
        tags = data.get('tags')
        # 添加标签
        add_article_tags(tags, article_obj)

        res['code'] = 0
        res['data'] = article_obj.nid
        return JsonResponse(res)

    # 编辑文章
    def put(self, request, nid):
        res = {
            'msg': '文章编辑成功',
            'code': 412,
            'data': None
        }

        article_query = Articles.objects.filter(nid=nid)
        if not article_query:
            res['msg'] = '请求错误'
            return JsonResponse(res)

        data = request.data
        data['status'] = 1
        form = AddArticleForm(data)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 校验通过
        article_query.update(**form.cleaned_data)
        tags = data.get('tags')
        # 标签修改(把以前的标签清空，然后重新写上去)
        article_query.first().tag.clear()
        # 添加标签
        add_article_tags(tags, article_query.first())

        res['code'] = 0
        res['data'] = article_query.first().nid
        return JsonResponse(res)


# 文章点赞
class ArticleDiggView(View):
    def post(self, request, nid):
        # nid 评论id
        res = {
            'msg': '点赞成功',
            'code': 412,
            'data': 0,
        }
        if not request.user.username:
            res['msg'] = '请登录'
            return JsonResponse(res)

        comment_query = Articles.objects.filter(nid=nid)
        comment_query.update(digg_count=F('digg_count') + 1)

        digg_count = comment_query.first().digg_count

        res['code'] = 0
        res['data'] = digg_count
        return JsonResponse(res)


# 文章收藏
class ArticleCollectsView(View):
    def post(self, request, nid):
        res = {
            'msg': '文章收藏成功',
            'code': 412,
            'isCollects': True,
            'data': 0,
        }
        if not request.user.username:
            res['msg'] = '请登录'
            return JsonResponse(res)

        # 判断用户是否收藏过文章
        flog = request.user.collects.filter(nid=nid)
        num = 1
        res['code'] = 0
        if flog:
            # 用户已经收藏了该文章，再次点击取消收藏
            res['msg'] = '文章取消收藏成功'
            res['isCollects'] = False
            request.user.collects.remove(nid)
            num = -1
        else:
            request.user.collects.add(nid)

        article_query = Articles.objects.filter(nid=nid)
        article_query.update(collects_count=F('collects_count') + num)
        collects_count = article_query.first().collects_count
        res['data'] = collects_count
        return JsonResponse(res)
