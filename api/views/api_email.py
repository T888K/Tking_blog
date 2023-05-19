from django.views import View
from django.http import JsonResponse
from api.views.login import clean_form
from django import forms
from django.core.mail import send_mail
import random
from TK_blog import settings
from django.core.handlers.wsgi import WSGIRequest
import time
from threading import Thread
from app01.models import UserInfo


class EmailForm(forms.Form):
    email = forms.EmailField(error_messages={'required': '请输入邮箱!', "invalid": '请输入正确的邮箱！'})

    def clean_email(self):
        email = self.cleaned_data['email']
        user = UserInfo.objects.filter(email=email)
        if user:
            self.add_error('email', '该邮箱已被绑定!')
        return email


class ApiEmail(View):
    def post(self, request: WSGIRequest):
        res = {
            'code': 502,
            'msg': '验证码获取成功！',
            'self': None,
        }
        form = EmailForm(request.data)
        if not form.is_valid():
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)

        # 发送邮箱成功 设置超时时间
        # 去session读取
        valid_email_obj = request.session.get('valid_email_obj')
        if valid_email_obj:
            time_stamp = valid_email_obj['time_stamp']
            now_stamp = time.time()
            # 时间戳相减
            if (now_stamp - time_stamp) < 40:
                res['msg'] = '请求过于频繁'
                return JsonResponse(res)

        # valid_email_code = ''.join(random.sample('0123456789', 6))
        valid_email_code = ''.join('876431')
        request.session["valid_email_obj"] = {
            'code': valid_email_code,
            'email': form.cleaned_data['email'],
            'time_stamp': time.time(),
        }
        print(valid_email_obj)

        Thread(target=send_mail, args=('【Tking_blog】您的反馈已被回复！请完善您的信息',
                                       f'【Tking_blog】您现在正在绑定邮箱，邮箱验证码位：{valid_email_code}',
                                       settings.EMAIL_HOST_USER,
                                       settings.EMAIL_PASSWORD,
                                       [form.cleaned_data.get('email')],
                                       False)).start()

        res['code'] = 0

        return JsonResponse(res)
