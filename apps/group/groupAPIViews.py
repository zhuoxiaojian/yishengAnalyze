from django.shortcuts import render

# Create your views here.
from group.serializers import GroupSerializer
from rest_framework.views import APIView
from utils.StandardPageNumberPaginationUtils import StandardPageNumberPagination
from rest_framework import status
from rest_framework.response import Response
from utils.apiAuth import TokenAuth
from groupMenu.models import GroupMenu
from django.contrib.auth.models import Group, Permission
from groupDepart.models import GroupDepart
from rest_framework.permissions import DjangoModelPermissions
class GroupApiView(APIView):
    queryset = Group.objects.all()
    authentication_classes = [TokenAuth, ]
    permission_classes = [DjangoModelPermissions, ]
    def get(self, request):
        name = request.GET.get("roleName")
        if not name is None:
            group = Group.objects.filter(name__icontains=name).order_by('id')
        else:
            group = Group.objects.all().order_by('id')
        pg = StandardPageNumberPagination()
        page_roles = pg.paginate_queryset(queryset=group, request=request, view=self)
        serializer = GroupSerializer(instance=page_roles, many=True)
        return pg.get_paginated_response(serializer.data)#Response(serializer.data)

    # post请求添加数据
    # 使用这个之后就会呈现一个post入口
    def post(self, request):
        data = request.data['params']
        # data = request.data
        # print(request.data['extraParams'])
        serializer = GroupSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            groupId = serializer.data['id']
            if 'extraParams' in request.data:
                extraData = request.data['extraParams']
                menuKey = None
                if 'menuKey' in extraData:
                    menuKey = extraData['menuKey']
                departKey = None
                if 'departKey' in extraData:
                    departKey = extraData['departKey']
                permissionsKey = None
                if 'permissionsKey' in extraData:
                    permissionsKey = extraData['permissionsKey']
                if not departKey is None:
                    GroupDepart.objects.create(group_id=groupId, depart_id=departKey)
                if menuKey:
                    querysetlist = []
                    for i in menuKey:
                        querysetlist.append(GroupMenu(group_id=groupId, menu_id=i))
                    GroupMenu.objects.bulk_create(querysetlist)
                if permissionsKey:
                    g = Group.objects.get(id=groupId)
                    for i in permissionsKey:
                        p = Permission.objects.get(id=i)
                        g.permissions.add(p)
                        g.save()


            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupDetail(APIView):
    queryset = Group.objects.all()
    authentication_classes = [TokenAuth, ]
    permission_classes = [DjangoModelPermissions, ]
    def get_object(self, pk):
        try:
            return Group.objects.get(pk=pk)
        except Exception as e:
            pass

    #http://localhost:8000/menu/menudetail/2/
    def get(self, request, pk):
        # print(request.user)
        group = self.get_object(pk)
        serializer = GroupSerializer(group)
        return Response(serializer.data)

    def put(self, request, pk):
        group = self.get_object(pk)
        data = request.data['params']
        # data = request.data
        # print(request.data['extraParams'])
        serializer = GroupSerializer(group, data=data)
        if serializer.is_valid():
            serializer.save()
            if 'extraParams' in request.data:
                extraData = request.data['extraParams']
                menuKey = None
                if 'menuKey' in extraData:
                    menuKey = extraData['menuKey']
                departKey = None
                if 'departKey' in extraData:
                    departKey = extraData['departKey']
                permissionsKey = None
                if 'permissionsKey' in extraData:
                    permissionsKey = extraData['permissionsKey']
                if not departKey is None:
                    rd = GroupDepart.objects.filter(group_id=group.id).first()
                    if not rd is None:
                        GroupDepart.objects.filter(id=rd.id).update(group_id=group.id, depart_id=departKey)
                    else:
                        GroupDepart.objects.create(group_id=group.id, depart_id=departKey)
                if menuKey:
                    GroupMenu.objects.filter(group=group).delete()
                    querysetlist = []
                    for i in menuKey:
                        querysetlist.append(GroupMenu(group_id=group.id, menu_id=i))
                    GroupMenu.objects.bulk_create(querysetlist)
                else:
                    GroupMenu.objects.filter(group=group).delete()

                if permissionsKey:
                    g = Group.objects.get(id=group.id)
                    g.permissions.clear()
                    for i in permissionsKey:
                        p = Permission.objects.get(id=i)
                        g.permissions.add(p)
                        g.save()

                else:
                    g = Group.objects.get(id=group.id)
                    g.permissions.clear()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        group = self.get_object(pk)
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


