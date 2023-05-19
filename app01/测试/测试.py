import os

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TK_blog.settings")
    import django
    django.setup()

    from app01.models import Moods
    from api.utils.get_user_info import get_addr_info

    mood_query = Moods.objects.all()
    for obj in mood_query:
        print(obj.addr, type(obj.addr))
        # addr = get_addr_info(obj.ip)
        # obj.addr = addr
        # obj.save()
