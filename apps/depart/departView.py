# -*- coding: utf-8 -*-
# @Time    : 2018/10/13 16:07
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : departView.py
# @Software: PyCharm
from django.views.decorators.csrf import csrf_exempt
from depart.models import Depart
from django.http import JsonResponse
from utils.jsonTreeUtils import initJsonTree
from django.db.models import Q
from utils.apiAuth import TokenAuth
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.views import APIView
@csrf_exempt
def checkDepartCode(request):
    response = {}
    departCode = request.GET.get('departCode')
    departId = request.GET.get('departId')
    r = None
    if not departId is None:
        r = Depart.objects.filter(~Q(id=departId), departCode=departCode)
    else:
        r = Depart.objects.filter(departCode=departCode)
    if r.exists():
        response['message'] = '该编码已占用'
        response['code'] = 300
    else:
        response['message'] = '该编码可用'
        response['code'] = 200
    return JsonResponse(response)

class initDepartTreeAPIView(APIView):
    queryset = Depart.objects.all()
    authentication_classes = [TokenAuth, ]
    permission_classes = [DjangoModelPermissions, ]
    def get(self, request):
        response = {}
        departs = Depart.objects.all()
        ret = initJsonTree(departs)
        response['message'] = ret
        response['code'] = 200
        return JsonResponse(response)