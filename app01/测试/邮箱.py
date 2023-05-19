import os

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TK_blog.settings")

    import django
    from django.core.mail import send_mail
    from TK_blog import settings

    django.setup()

    send_mail(
        '【Tking_blog】您的反馈已被回复！',
        '123456',
        settings.EMAIL_HOST_USER,
        ['990224205@qq.com'],
        False
    )
