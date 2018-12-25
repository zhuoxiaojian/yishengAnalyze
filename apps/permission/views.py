# -*- coding: utf-8 -*-
# @Time    : 2018/10/19 21:33
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : views.py
# @Software: PyCharm
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Permission
import json
from django.http import JsonResponse
from systemToken.models import SystemToken
#角色管理菜单中其它权限下拉框中的内容
@csrf_exempt
def getAllPermission(request):
    response = {}
    http_token = request.META.get("HTTP_AUTHORIZATION")
    token_obj = SystemToken.objects.filter(token=http_token).first()
    # 验证失败
    if not token_obj:
        return JsonResponse(response)
    result_set = Permission.objects.all().values('id', 'codename')
    result_json = json.dumps(list(result_set))
    response['permissionJson'] = result_json
    return JsonResponse(response)