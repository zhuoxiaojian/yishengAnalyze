# -*- coding: utf-8 -*-
# @Time    : 2018/12/25 11:45
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : contentTypeView.py
# @Software: PyCharm
from django.http import JsonResponse
from django.contrib.auth.models import ContentType
from utils.apiAuth import TokenAuth
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.views import APIView
import json
class getAllContentTypeAPIView(APIView):
    queryset = ContentType.objects.all()
    authentication_classes = [TokenAuth, ]
    permission_classes = [DjangoModelPermissions, ]
    def get(self, request):
        response = {}
        list = []
        contentType = ContentType.objects.all()
        for content in contentType:
            _dict = {}
            _dict['id'] = content.id
            _dict['model'] = content.model
            list.append(_dict)
        response['result'] = json.dumps(list)
        return JsonResponse(response)
