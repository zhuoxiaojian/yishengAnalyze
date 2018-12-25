# -*- coding: utf-8 -*-
# @Time    : 2018/12/25 13:35
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : contentTypeAPIViews.py
# @Software: PyCharm
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.StandardPageNumberPaginationUtils import StandardPageNumberPagination
from utils.apiAuth import TokenAuth
from django.contrib.auth.models import ContentType
from contentType.serializers import ContentTypeSerializer
from rest_framework.permissions import DjangoModelPermissions
import logging
logger = logging.getLogger(__name__)

class ContentTypeApiView(APIView):
    queryset = ContentType.objects.all()
    authentication_classes = [TokenAuth, ]
    permission_classes = [DjangoModelPermissions, ]
    def get(self, request):
        contentTypeName = request.GET.get("contentTypeName")
        if not contentTypeName is None:
            contentType = ContentType.objects.filter(model__icontains=contentTypeName).order_by('id')
        else:
            contentType = ContentType.objects.all().order_by('id')
        pg = StandardPageNumberPagination()
        page_roles = pg.paginate_queryset(queryset=contentType, request=request, view=self)
        serializer = ContentTypeSerializer(instance=page_roles, many=True)
        return pg.get_paginated_response(serializer.data)#Response(serializer.data)

    # post请求添加数据
    # 使用这个之后就会呈现一个post入口
    def post(self, request):
        data = request.data
        serializer = ContentTypeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # print(serializer.data['id'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContentTypeDetail(APIView):
    queryset = ContentType.objects.all()
    authentication_classes = [TokenAuth, ]
    permission_classes = [DjangoModelPermissions, ]
    def get_object(self, pk):
        try:
            return ContentType.objects.get(pk=pk)
        except Exception as e:
            pass

    #http://localhost:8000/menu/menudetail/2/
    def get(self, request, pk):
        contentType = self.get_object(pk)
        serializer = ContentTypeSerializer(contentType)
        return Response(serializer.data)

    def put(self, request, pk):
        contentType = self.get_object(pk)
        serializer = ContentTypeSerializer(contentType, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # logger.error('-----------------------'+str(request.user)+'修改实体--------------------------------')
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        contentType = self.get_object(pk)
        contentType.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)