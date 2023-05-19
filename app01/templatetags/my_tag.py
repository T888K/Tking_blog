from django import template
from app01.utils.search import Search
from django.utils.safestring import mark_safe
from app01.models import Tags, Avatars, Menu

register = template.Library()


@register.inclusion_tag('my_tag/headers.html')
def banner(menu_name, article=None):
    if article:
        # 进入了说明时文章详情页面
        # 拿到文章封面
        cover = article.cover.url.url
        img_list = [cover]
        title = article.title
        slogan_list = [article.abstract[:50]]
        return locals()

    menu_obj = Menu.objects.get(menu_title_en=menu_name)
    img_list = [i.url.url for i in menu_obj.menu_url.all()]
    menu_time = menu_obj.menu_time
    title = menu_obj.title

    slogan_list = menu_obj.abstract.replace('；', ';').replace('\n', ';').split(';')
    slogan_time = menu_obj.abstract_time

    if not menu_obj.menu_rotation:
        # 图片不要轮播
        img_list = img_list[0:1]
        menu_time = 0

    if not menu_obj.rotation:
        # slogan不轮播
        slogan_list = slogan_list[0:1]
        slogan_time = 0

    return locals()


# 生成标签
@register.simple_tag
def generate_order_html(request, key):
    order = request.GET.get(key, '')
    order_list = []
    if key == 'order':
        order_list = [
            ('', '综合排序'),
            ('-create_date', '最新发布'),
            ('-look_count', '最多浏览'),
            ('-digg_count', '最多点赞'),
            ('-collects_count', '最多收藏'),
            ('-comment_count', '最多评论')
        ]
    elif key == 'word':
        order = request.GET.getlist(key, '')
        order_list = [
            ([''], '全部字数'),
            (['0', '100'], '100字以内'),
            (['100', '500'], '500字以内'),
            (['500', '1000'], '1000字以内'),
            (['1000', '3000'], '3000字以内'),
            (['3000', '5000'], '5000字以内')
        ]
    elif key == 'tag':
        tag_list = Tags.objects.exclude(articles__isnull=True)
        order_list.append(('', '全部标签'))
        for tag in tag_list:
            order_list.append((tag.title, tag.title))

    query_params = request.GET.copy()

    order = Search(
        key=key,
        order=order,
        order_list=order_list,
        query_params=query_params
    )
    return mark_safe(order.order_html())


# 生成动态导航
@register.simple_tag
def dynamic_navigation(request):
    path = request.path_info
    path_dict = {
        '/': '首页',
        '/news/': '新闻',
        '/moods/': '心情',
        '/history/': '回忆录',
        '/about/': '关于',
        '/search/?word=': '文章搜索',
        '/sites/': '网站导航',
    }

    nav_list = []
    for k, v in path_dict.items():
        if k == path:
            nav_list.append(f'<a href="{k}" class="actives" style="color: #ff9800">{v}</a>')
            continue
        nav_list.append(f'<a href="{k}">{v}</a>')
    return mark_safe(''.join(nav_list))


# 生成广告
@register.simple_tag
def generate_advert(advert_list):
    html_list = []
    for i in advert_list:
        if i.img:
            html_list.append(f'<div><a href="{i.href}" title="{i.title}" target="_blank"><img src="{i.img.url}" alt=""></a></div>')
            continue
        html_s: str = i.img_list
        html_new = html_s.replace('；', ';').replace('\n', ';')
        img_list = html_new.split(';')
        for url in img_list:
            html_list.append(f'<div><a href="{i.href}" title="{i.title}" target="_blank"><img src="{url}" alt=""></a></div>')
    return mark_safe(''.join(html_list))


# 配置心情选图
@register.simple_tag
def generate_drawing(drawing: str):
    if not drawing:
        return ''
    drawing = drawing.replace('；', ';').replace('\n', ';')
    drawing_list = drawing.split(';')
    html_s = ''
    for i in drawing_list:
        html_s += f'<img src="{i}" alt="">'
    return mark_safe(html_s)

# 生成标签
@register.simple_tag
def generate_tag_html():
    tag_list = Tags.objects.all()[:15]
    tag_html = []
    for tag in tag_list:
        if tag.articles_set.all():
            tag_html.append(f'<li>{tag.title} <i style="display: flex;justify-content: center;align-items: center;width: 20px;height: 20px;font-size: 10px;color: #ffffff;background-color: #01b0b7 ;border-radius: 50%;margin-left: 5px;">{tag.articles_set.count()}</i></li>')
        else:
            tag_html.append(f'<li>{tag.title}</li>')
    return mark_safe(''.join(tag_html))

