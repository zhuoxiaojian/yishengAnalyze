from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from constant.models import Constant
from constant.serializers import ConstantSerializer
from utils.StandardPageNumberPaginationUtils import StandardPageNumberPagination
from utils.apiAuth import TokenAuth
from rest_framework.permissions import DjangoModelPermissions
class ConstantApiView(APIView):
    queryset = Constant.objects.all()
    authentication_classes = [TokenAuth, ]
    permission_classes = [DjangoModelPermissions, ]
    def get(self, request):
        constantName = request.GET.get("constantName")
        if not constantName is None:
            constant = Constant.objects.filter(name__icontains=constantName).order_by('id')
        else:
            constant = Constant.objects.all().order_by('id')

        pg = StandardPageNumberPagination()
        page_roles = pg.paginate_queryset(queryset=constant, request=request, view=self)
        serializer = ConstantSerializer(instance=page_roles, many=True)
        return pg.get_paginated_response(serializer.data)#Response(serializer.data)

    # post请求添加数据
    # 使用这个之后就会呈现一个post入口
    def post(self, request):
        data = request.data
        serializer = ConstantSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # print(serializer.data['id'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ConstantDetail(APIView):
    queryset = Constant.objects.all()
    authentication_classes = [TokenAuth, ]
    permission_classes = [DjangoModelPermissions, ]
    def get_object(self, pk):
        try:
            return Constant.objects.get(pk=pk)
        except Exception as e:
            pass

    #http://localhost:8000/menu/menudetail/2/
    def get(self, request, pk):
        constant = self.get_object(pk)
        serializer = ConstantSerializer(constant)
        return Response(serializer.data)

    def put(self, request, pk):
        constant = self.get_object(pk)
        serializer = ConstantSerializer(constant, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        constant = self.get_object(pk)
        constant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)