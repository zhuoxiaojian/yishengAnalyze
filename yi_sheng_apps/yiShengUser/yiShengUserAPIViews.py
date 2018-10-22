# -*- coding: utf-8 -*-
# @Time    : 2018/10/22 14:45
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : yiShengUserAPIViews.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
# @Time    : 2018/10/19 21:31
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : permissionAPIViews.py.py
# @Software: PyCharm
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.StandardPageNumberPaginationUtils import StandardPageNumberPagination
from utils.apiAuth import TokenAuth
from yiShengUser.models import YiShengUser
from yiShengUser.serializers import YiShengUserSerializer
from rest_framework.permissions import DjangoModelPermissions
class YiShengUserApiView(APIView):
    queryset = YiShengUser.objects.all()
    authentication_classes = [TokenAuth, ]
    permission_classes = [DjangoModelPermissions, ]
    def get(self, request):
        yiShengUser = YiShengUser.objects.all().order_by('id')
        pg = StandardPageNumberPagination()
        page_roles = pg.paginate_queryset(queryset=yiShengUser, request=request, view=self)
        serializer = YiShengUserSerializer(instance=page_roles, many=True)
        return pg.get_paginated_response(serializer.data)#Response(serializer.data)

    # post请求添加数据
    # 使用这个之后就会呈现一个post入口
    def post(self, request):
        data = request.data
        serializer = YiShengUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # print(serializer.data['id'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class YiShengUserDetail(APIView):
    queryset = YiShengUser.objects.all()
    authentication_classes = [TokenAuth, ]
    permission_classes = [DjangoModelPermissions, ]
    def get_object(self, pk):
        try:
            return YiShengUser.objects.get(pk=pk)
        except Exception as e:
            pass

    #http://localhost:8000/menu/menudetail/2/
    def get(self, request, pk):
        yiShengUser = self.get_object(pk)
        serializer = YiShengUserSerializer(yiShengUser)
        return Response(serializer.data)

    def put(self, request, pk):
        yiShengUser = self.get_object(pk)
        serializer = YiShengUserSerializer(yiShengUser, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        yiShengUser = self.get_object(pk)
        yiShengUser.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)