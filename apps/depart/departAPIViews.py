from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from depart.models import Depart
from depart.serializers import DepartSerializer
from utils.StandardPageNumberPaginationUtils import StandardPageNumberPagination
from utils.apiAuth import TokenAuth
from rest_framework.permissions import DjangoModelPermissions
class DepartApiView(APIView):
    queryset = Depart.objects.all()
    authentication_classes = [TokenAuth, ]
    permission_classes = [DjangoModelPermissions, ]
    def get(self, request):
        depart = Depart.objects.all().order_by('id')
        pg = StandardPageNumberPagination()
        page_roles = pg.paginate_queryset(queryset=depart, request=request, view=self)
        serializer = DepartSerializer(instance=page_roles, many=True)
        return pg.get_paginated_response(serializer.data)#Response(serializer.data)

    # post请求添加数据
    # 使用这个之后就会呈现一个post入口
    def post(self, request):
        data = request.data
        serializer = DepartSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # print(serializer.data['id'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DepartDetail(APIView):
    queryset = Depart.objects.all()
    authentication_classes = [TokenAuth, ]
    permission_classes = [DjangoModelPermissions, ]
    def get_object(self, pk):
        try:
            return Depart.objects.get(pk=pk)
        except Exception as e:
            pass

    #http://localhost:8000/menu/menudetail/2/
    def get(self, request, pk):
        print(request.user)
        depart = self.get_object(pk)
        serializer = DepartSerializer(depart)
        return Response(serializer.data)

    def put(self, request, pk):
        depart = self.get_object(pk)
        serializer = DepartSerializer(depart, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        depart = self.get_object(pk)
        departChildren = Depart.objects.filter(parentId=depart.id)
        if depart.is_parent and departChildren.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            depart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


