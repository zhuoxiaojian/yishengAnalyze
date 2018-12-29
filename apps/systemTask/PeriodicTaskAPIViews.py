# -*- coding: utf-8 -*-
# @Time    : 2018/12/28 14:37
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : IntervalScheduleAPIViews.py
# @Software: PyCharm
from djcelery.models import PeriodicTask
from rest_framework.views import APIView
from utils.StandardPageNumberPaginationUtils import StandardPageNumberPagination
from rest_framework import status
from rest_framework.response import Response
from utils.apiAuth import TokenAuth
from rest_framework.permissions import DjangoModelPermissions
from systemTask.PeriodicTaskSerializers import PeriodicTaskSerializer
class PeriodicTaskAPIView(APIView):
    queryset = PeriodicTask.objects.all()
    authentication_classes = [TokenAuth, ]
    permission_classes = [DjangoModelPermissions, ]
    def get(self, request):
        periodicTaskName = request.GET.get('periodicTaskName')
        if periodicTaskName:
            periodicTask = PeriodicTask.objects.filter(name__icontains=periodicTaskName).order_by('id')
        else:
            periodicTask = PeriodicTask.objects.all().order_by('id')
        pg = StandardPageNumberPagination()
        page_roles = pg.paginate_queryset(queryset=periodicTask, request=request, view=self)
        serializer = PeriodicTaskSerializer(instance=page_roles, many=True)
        return pg.get_paginated_response(serializer.data)
    def post(self, request):
        data = request.data
        serializer = PeriodicTaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # print(serializer.data['id'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PeriodicTaskDetail(APIView):
    queryset = PeriodicTask.objects.all()
    authentication_classes = [TokenAuth, ]
    permission_classes = [DjangoModelPermissions, ]
    def get_object(self, pk):
        try:
            return PeriodicTask.objects.get(pk=pk)
        except Exception as e:
            pass

    #http://localhost:8000/menu/menudetail/2/
    def get(self, request, pk):
        periodicTask = self.get_object(pk)
        serializer = PeriodicTaskSerializer(periodicTask)
        return Response(serializer.data)

    def put(self, request, pk):
        periodicTask = self.get_object(pk)
        serializer = PeriodicTaskSerializer(periodicTask, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        periodicTask = self.get_object(pk)
        periodicTask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)