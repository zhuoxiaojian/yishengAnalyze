# -*- coding: utf-8 -*-
# @Time    : 2018/10/13 16:02
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : constantView.py
# @Software: PyCharm
from django.views.decorators.csrf import csrf_exempt
from constant.models import Constant
from django.db.models import Q
from django.http import JsonResponse
@csrf_exempt
def checkConstantName(request):
    response = {}
    constantName = request.GET.get('constantName')
    constantId = request.GET.get('constantId')
    r = None
    if not constantId is None:
        r = Constant.objects.filter(~Q(id=constantId), name=constantName)
    else:
        r = Constant.objects.filter(name=constantName)
    if r.exists():
        response['message'] = '键名已占用'
        response['code'] = 300
    else:
        response['message'] = '键名可用'
        response['code'] = 200
    return JsonResponse(response)