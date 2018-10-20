# -*- coding: utf-8 -*-
# @Time    : 2018/9/21 17:13
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : userView.py
# @Software: PyCharm
from users.models import UserProfile
from users.serializers import UserProfileSerializer
from rest_framework.views import APIView
from utils.StandardPageNumberPaginationUtils import StandardPageNumberPagination
from rest_framework import status
from rest_framework.response import Response
from utils.apiAuth import TokenAuth
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import DjangoModelPermissions
from django.contrib.auth.models import Group
class UserProfileApiView(APIView):
    queryset = UserProfile.objects.all()
    authentication_classes = [TokenAuth, ]
    permission_classes = [DjangoModelPermissions, ]
    def get(self, request):
        username = request.GET.get("userName")
        if not username is None:
            user = UserProfile.objects.filter(username__icontains=username).order_by('id')
        else:
            user = UserProfile.objects.all().order_by('id')
        pg = StandardPageNumberPagination()
        page_roles = pg.paginate_queryset(queryset=user, request=request, view=self)
        serializer = UserProfileSerializer(instance=page_roles, many=True)
        return pg.get_paginated_response(serializer.data)#Response(serializer.data)

    # post请求添加数据
    # 使用这个之后就会呈现一个post入口
    def post(self, request):
        # data = request.data
        data = request.data['params']
        data['password'] = make_password(data['password'])
        serializer = UserProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            userId = serializer.data['id']
            if 'extraParams' in request.data:
                extraData = request.data['extraParams']
                if 'userRoleParams' in extraData:
                    userRoleParams = extraData['userRoleParams']
                    if not userRoleParams is None:
                        u = UserProfile.objects.get(id=userId)
                        g = Group.objects.get(id=int(userRoleParams))
                        u.groups.add(g)
                        u.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileDetail(APIView):
    queryset = UserProfile.objects.all()
    authentication_classes = [TokenAuth, ]
    permission_classes = [DjangoModelPermissions, ]
    def get_object(self, pk):
        try:
            return UserProfile.objects.get(pk=pk)
        except Exception as e:
            pass

    #http://localhost:8000/menu/menudetail/2/
    def get(self, request, pk):
        print(request.user)
        user = self.get_object(pk)
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        data = request.data['params']
        serializer = UserProfileSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            if user.is_superuser:
                pass
            else:
                if 'extraParams' in request.data:
                    extraData = request.data['extraParams']
                    if 'userRoleParams' in extraData:
                        userRoleParams = extraData['userRoleParams']
                        if not userRoleParams is None:
                            g = Group.objects.get(id=userRoleParams)
                            u = UserProfile.objects.get(id=pk)
                            u.groups.clear()
                            u.groups.add(g)
                            u.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        # UserRole.objects.filter(user_id=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)