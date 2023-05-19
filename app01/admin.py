from django.contrib import admin
from app01.models import *
# from app01.models import Articles
# from app01.models import Tags  # 文章标签
# from app01.models import Cover  # 文章封面
# from app01.models import Comment  # 文章评论
# from app01.models import Avatars  # 头像
# from app01.models import UserInfo  # 用户
from django.utils.safestring import mark_safe


# Register your models here.

# 文章
class ArticleAdmin(admin.ModelAdmin):
    def get_cover(self):
        if self.cover:
            return mark_safe(f'<img src="{self.cover.url.url}" style="height:60px;width:100px;border-radius:5px;">')
        return

    get_cover.short_description = '文章封面'

    def get_tags(self):
        tag_list = ','.join([i.title for i in self.tag.all()])
        return tag_list

    get_tags.short_description = '文章标签'

    def get_title(self):
        return mark_safe(f'<a href="/article/{self.nid}/" target="_blank">{self.title}</a>')

    get_title.short_description = '文章标题'

    def get_edit_delete_btn(self):
        return mark_safe(f"""
        <a href="/backend/edit_article/{self.nid}/" target="_blank">编辑</a>
        <a href="/admin/app01/articles/{self.nid}/delete/">删除</a>
        """)

    get_edit_delete_btn.short_description = '操作'

    list_display = [
        get_title,
        get_cover,
        get_tags,
        'category',
        'look_count',
        'digg_count',
        'collects_count',
        'word',
        'change_date',
        get_edit_delete_btn
    ]

    def action_word(self, request, queryset):
        for obj in queryset:
            word = len(obj.content)
            obj.word = word
            obj.save()

    action_word.short_description = '获取文章字数'
    action_word.type = 'success'
    actions = [action_word]


admin.site.register(Articles, ArticleAdmin)

admin.site.register(Tags)
admin.site.register(Cover)
admin.site.register(Comment)
admin.site.register(Avatars)


# 用户信息
class UserInfoAdmin(admin.ModelAdmin):
    def get_avatar(self: UserInfo):
        if self.sign_status in [1, 2]:
            return mark_safe(f'<img src="{self.avatar_url}" style="width:30px;height:30px;border-radius:50%;">')

        if self.avatar:
            return mark_safe(f'<img src="{self.avatar.url.url}" style="width:30px;height:30px;border-radius:50%;">')

    get_avatar.short_description = '头像'

    def get_user_name(self):
        if not self.sign_status:
            return self.username
        return '****'

    get_user_name.short_description = '用户名'

    list_display = [get_user_name, get_avatar, 'sign_status', 'ip', 'addr', 'is_superuser', 'date_joined',
                    'last_login']

    # 获取头像
    def get_avatar_action(self, request, queryset):
        for obj in queryset:
            if not obj.sign_status:
                continue
            # 其他平台注册的

    get_avatar_action.short_description = '获取用户信息'
    actions = [get_avatar_action]


admin.site.register(UserInfo, UserInfoAdmin)


# 广告
class AdvertAdmin(admin.ModelAdmin):

    def get_href(self):
        return mark_safe(f"""<a href="{self.href}" target="_blank">跳转链接</a>""")

    get_href.short_description = '跳转链接'

    def get_img_list(self):
        html_s: str = self.img_list
        html_new = html_s.replace('；', ';').replace('\n', ';')
        img_list = html_new.split(';')

        html_str = ''
        for i in img_list:
            html_str += f'<img src="{i}" style="height:60px;border-radius:5px;margin-right:10px;">'
        return mark_safe(html_str)

    get_img_list.short_description = '广告封面'

    def get_img(self):
        if self.img:
            return mark_safe(f"""<img src="{self.img.url}" style="height:60px;border-radius:5px;">""")

    get_img.short_description = '用户上传图片'

    list_display = [
        'title',
        get_img,
        'is_show',
        'author',
        get_img_list,
        get_href,
    ]


admin.site.register(Advert, AdvertAdmin)


class MenuImgAdmin(admin.ModelAdmin):
    def get_img(self):
        if self.url:
            return mark_safe(f"""<img src="{self.url.url}" style="height:60px;border-radius:5px;">""")

    get_img.short_description = '站点背景图片'
    list_display = ['url', get_img]


# 站点背景图片
admin.site.register(MenuImg, MenuImgAdmin)


class MenuAdmin(admin.ModelAdmin):
    def get_menu_url(self: Menu):
        lis = [f"<img src='{i.url.url}' style='height:60px;border-radius:5px;margin-right:5px;margin-bottom:5px;'>" for i in
               self.menu_url.all()]
        return mark_safe(''.join(lis))

    get_menu_url.short_description = '图片组'
    list_display = ['menu_title', 'menu_title_en',
                    'title', 'abstract',
                    'rotation', "abstract_time",
                    'menu_rotation', 'menu_time', get_menu_url]


# 站点背景
admin.site.register(Menu, MenuAdmin)
