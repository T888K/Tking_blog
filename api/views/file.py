from django.views import View
from django.http import JsonResponse
from app01.models import Avatars, Cover, UserInfo
from django.core.files.uploadedfile import InMemoryUploadedFile
from app01.models import avatar_delete, cover_delete
from django.db.models import Q
import base64
from api.utils.api_qiniu import upload_data


# 头像
class AvatarView(View):
    def post(self, request):
        res = {
            'code': 501,
            'msg': '文件上传失败'
        }

        if not request.user.is_superuser:
            res['msg'] = '用户验证失败'
            return JsonResponse(res)

        file: InMemoryUploadedFile = request.FILES.get('file')
        name: str = file.name
        white_file_type = {
            'jpg', 'jpeg', 'png'
        }
        if name.split('.')[-1] not in white_file_type:
            return JsonResponse(res)

        kb = file.size / 1024 / 1024
        if kb > 2:
            res['msg'] = '文件大小超过2MB！'
            return JsonResponse(res)

        Avatars.objects.create(url=file)
        res['code'] = 0
        res['msg'] = '头像上传成功！'
        return JsonResponse(res)

    def delete(self, request, nid):
        print(nid)
        res = {
            'code': 501,
            'msg': '头像删除成功！'
        }

        if not request.user.is_superuser:
            res['msg'] = '用户验证失败'
            return JsonResponse(res)

        avatar_query = Avatars.objects.filter(nid=nid)
        if not avatar_query:
            res['msg'] = '头像已被删除！'
            return JsonResponse(res)

        # 判断图片是否使用
        obj: Avatars = avatar_query.first()
        user_query = UserInfo.objects.filter(Q(sign_status=1) | Q(sign_status=2))
        for user in user_query:
            if obj.url.url == user.avatar_url:
                res['msg'] = '该头像已被使用!'
                return JsonResponse(res)

        avatar_delete(avatar_query.first())
        avatar_query.delete()

        res['code'] = 0
        return JsonResponse(res)


# 封面
class CoverView(View):
    def post(self, request):
        res = {
            'code': 501,
            'msg': '文件上传失败'
        }

        if not request.user.is_superuser:
            res['msg'] = '用户验证失败'
            return JsonResponse(res)

        file: InMemoryUploadedFile = request.FILES.get('file')
        name: str = file.name
        white_file_type = {
            'jpg', 'jpeg', 'png'
        }
        if name.split('.')[-1] not in white_file_type:
            return JsonResponse(res)

        kb = file.size / 1024 / 1024
        if kb > 10:
            res['msg'] = '文件大小超过10MB！'
            return JsonResponse(res)

        Cover.objects.create(url=file)
        res['code'] = 0
        res['msg'] = '封面上传成功'
        return JsonResponse(res)

    def delete(self, request, nid):
        print(nid)
        res = {
            'code': 501,
            'msg': '封面删除成功！'
        }

        if not request.user.is_superuser:
            res['msg'] = '用户验证失败'
            return JsonResponse(res)

        cover_query = Cover.objects.filter(nid=nid)
        if not cover_query:
            res['msg'] = '封面已被删除！'
            return JsonResponse(res)
        cover_delete(cover_query.first())
        cover_query.delete()

        res['code'] = 0
        return JsonResponse(res)


# 粘贴上传
class PasteUpload(View):
    def post(self, request):
        img = request.data.get('image')
        ines = img.split('base64,')
        imgData = base64.b64decode(ines[1])
        url = upload_data(imgData)
        return JsonResponse({'url': url})
