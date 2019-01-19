# -*- coding: utf-8 -*-
# @Time    : 2019/1/17 13:51
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : systemMessageViews.py
# @Software: PyCharm
from utils.apiAuth import TokenAuth
from rest_framework.permissions import DjangoModelPermissions
from .models import SystemMessage
from .serializers import SystemMessageSerializer
from django.http import JsonResponse
from rest_framework.views import APIView

class SystemMessageView(APIView):
    queryset = SystemMessage.objects.all().order_by('id')
    authentication_classes = [TokenAuth, ]
    # permission_classes = [DjangoModelPermissions, ]

    def get(self, request):
        flagParams = request.GET.get('flagParams')
        response = {}
        result_list = []
        queryset = SystemMessage.objects.all().order_by('id')
        if flagParams:
            flags = flagParams.split(',')
            if flags:
                for flag in flags:
                    flag_reslut = {}
                    if flag:
                        result_dict = {}
                        list = []
                        queryset = SystemMessage.objects.filter(flag=int(flag))
                        if queryset.exists():
                            for q in queryset:
                                data = {}
                                data['id'] = q.id
                                data['message_info'] = q.message_info
                                data['flag'] = q.flag
                                data['create_date'] = q.create_date
                                list.append(data)
                        result_dict['flag'+str(flag)+'Data'] = list
                        result_dict['flag'+str(flag)+'Count'] = len(list)
                        flag_dict = {}
                        flag_dict['flag'+str(flag)] = result_dict
                        result_list.append(flag_dict)
        response['resultData'] = result_list
        return JsonResponse(response)

    def post(self, request):
        methodParams = request.data['methodParams']
        dataParams = request.data['dataParams']
        response = {}
        if "unreadToread" == methodParams:
            SystemMessage.objects.filter(id=dataParams).update(flag=1)
            response['code'] = 200
            response['message'] = '标记成功'
        elif "readToRecycle" == methodParams:
            SystemMessage.objects.filter(id=dataParams).update(flag=2)
            response['code'] = 200
            response['message'] = '回收成功'
        elif "recycleToRead" == methodParams:
            SystemMessage.objects.filter(id=dataParams).update(flag=1)
            response['code'] = 200
            response['message'] = '还原成功'
        elif "recycleToDeleteAll" in methodParams:
            SystemMessage.objects.extra(where=['id IN (' + dataParams + ')']).delete()
            response['code'] = 200
            response['message'] = '全部清空成功'
        elif "readToRecycleAll" == methodParams:
            SystemMessage.objects.extra(where=['id IN (' + dataParams + ')']).update(flag=2)
            response['code'] = 200
            response['message'] = '全部回收成功'
        elif "allToRead" == methodParams:
            SystemMessage.objects.extra(where=['id IN (' + dataParams + ')']).update(flag=1)
            response['code'] = 200
            response['message'] = '全部标记成功'
        return JsonResponse(response)