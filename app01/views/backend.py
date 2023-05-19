from django.shortcuts import render, redirect
from app01.models import *

# 后台
def backend(request):
    # 如果没有登录，不能去个人中心
    if not request.user.username:
        return redirect('/')

    user = request.user
    collects_query = user.collects.all()

    return render(request, 'backend/backend.html', locals())


def add_article(request):
    # 拿到所有分类，标签
    tag_list = Tags.objects.all()
    # 拿到所有的文章封面
    cover_list = Cover.objects.all()
    c_l = []
    for cover in cover_list:
        c_l.append({
            "url": cover.url.url,
            "nid": cover.nid
        })

    category_list = Articles.category_choice
    return render(request, 'backend/add_article.html', locals())


def edit_avatar(request):
    # 查询所有头像
    avatar_list = Avatars.objects.all()

    user = request.user
    sign_status = user.sign_status
    if sign_status == 0:
        # 本地用户名注册
        avatar_id = request.user.avatar.nid
    else:
        # 第三方注册
        avatar_url = request.user.avatar_url
        for i in avatar_list:
            if i.url.url == avatar_url:
                avatar_id = i.nid
    return render(request, 'backend/edit_avatar.html', locals())


def reset_password(request):
    return render(request, 'backend/reset_password.html', locals())


def edit_article(request, nid):
    article_obj = Articles.objects.get(nid=nid)
    tags = [str(tag.nid) for tag in article_obj.tag.all()]

    # 拿到所有分类，标签
    tag_list = Tags.objects.all()
    # 拿到所有的文章封面
    cover_list = Cover.objects.all()
    c_l = []
    for cover in cover_list:
        c_l.append({
            "url": cover.url.url,
            "nid": cover.nid
        })

    category_list = Articles.category_choice

    return render(request, 'backend/edit_article.html', locals())


# 头像列表
def avatar_list(request):
    # 查询所有头像
    avatar_query = Avatars.objects.all()
    return render(request, 'backend/avatar_list.html', locals())


# 文章封面
def cover_list(request):
    cover_query = Cover.objects.all()
    return render(request, 'backend/cover_list.html', locals())


def admin_home(request):
    return render(request, 'admin_home.html')
