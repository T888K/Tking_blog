"""
URL configuration for TK_blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from app01.views import index, backend
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_home/', backend.admin_home),
    path('', index.index),
    path('news/', index.news),
    path('moods/', index.moods),
    path('history/', index.history),
    path('login/random_code/', index.get_random_code),
    path('login/', index.login),
    path('sign/', index.sign),
    path('logout/', index.logout),
    path('search/', index.search),
    path('sites/', index.sites),

    # 文章详情
    re_path(r'^article/(?P<nid>\d+)/', index.article),

    # 后台个人中心
    path('backend/', backend.backend),
    # 后台添加文章
    path('backend/add_article/', backend.add_article),
    # 后台修改头像
    path('backend/edit_avatar/', backend.edit_avatar),
    # 后台重置密码
    path('backend/reset_password/', backend.reset_password),
    # 后台头像列表
    path('backend/avatar_list/', backend.avatar_list),
    # 后台封面列表
    path('backend/cover_list/', backend.cover_list),

    # 编辑文章
    re_path(r'^backend/edit_article/(?P<nid>\d+)', backend.edit_article),

    # 路由分发 把所有api开头的请求发送到api这个urls.py中
    re_path(r'^api/', include('api.urls')),

    # 用户上传文件路由配置
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
