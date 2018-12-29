# -*- coding: utf-8 -*-
# @Time    : 2018/12/29 11:52
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : TaskStateAPIViews.py
# @Software: PyCharm
from djcelery.models import TaskState
from rest_framework.views import APIView
from utils.StandardPageNumberPaginationUtils import StandardPageNumberPagination
from utils.apiAuth import TokenAuth
from rest_framework.permissions import DjangoModelPermissions
from systemTask.TaskStateSerializers import TaskStateSerializer
class TaskStateAPIView(APIView):
    queryset = TaskState.objects.all()
    authentication_classes = [TokenAuth, ]
    permission_classes = [DjangoModelPermissions, ]
    def get(self, request):
        taskStateName = request.GET.get('taskStateName')
        if taskStateName:
            taskState = TaskState.objects.filter(name__icontains=taskStateName).order_by('id')
        else:
            taskState = TaskState.objects.all().order_by('id')
        pg = StandardPageNumberPagination()
        page_roles = pg.paginate_queryset(queryset=taskState, request=request, view=self)
        serializer = TaskStateSerializer(instance=page_roles, many=True)
        return pg.get_paginated_response(serializer.data)