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
from django.contrib.auth.models import Permission
from permission.serializers import PermissionSerializer
from rest_framework.permissions import DjangoModelPermissions
class PermissionApiView(APIView):
    queryset = Permission.objects.all()
    authentication_classes = [TokenAuth, ]
    permission_classes = [DjangoModelPermissions, ]
    def get(self, request):
        permission = Permission.objects.all().order_by('id')
        pg = StandardPageNumberPagination()
        page_roles = pg.paginate_queryset(queryset=permission, request=request, view=self)
        serializer = PermissionSerializer(instance=page_roles, many=True)
        return pg.get_paginated_response(serializer.data)#Response(serializer.data)

    # post请求添加数据
    # 使用这个之后就会呈现一个post入口
    def post(self, request):
        data = request.data
        serializer = PermissionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # print(serializer.data['id'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PermissionDetail(APIView):
    queryset = Permission.objects.all()
    authentication_classes = [TokenAuth, ]
    permission_classes = [DjangoModelPermissions, ]
    def get_object(self, pk):
        try:
            return Permission.objects.get(pk=pk)
        except Exception as e:
            pass

    #http://localhost:8000/menu/menudetail/2/
    def get(self, request, pk):
        permission = self.get_object(pk)
        serializer = PermissionSerializer(permission)
        return Response(serializer.data)

    def put(self, request, pk):
        permission = self.get_object(pk)
        serializer = PermissionSerializer(permission, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        permission = self.get_object(pk)
        permission.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)