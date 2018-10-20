from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from menu.models import Menu
from menu.serializers import MenuSerializer
from utils.StandardPageNumberPaginationUtils import StandardPageNumberPagination
from utils.apiAuth import TokenAuth
from rest_framework.permissions import DjangoModelPermissions
class MenuApiView(APIView):
    queryset = Menu.objects.all()
    authentication_classes = [TokenAuth, ]
    permission_classes = [DjangoModelPermissions, ]
    def get(self, request):
        menu = Menu.objects.all().order_by('id')
        pg = StandardPageNumberPagination()
        page_roles = pg.paginate_queryset(queryset=menu, request=request, view=self)
        serializer = MenuSerializer(instance=page_roles, many=True)
        return pg.get_paginated_response(serializer.data)#Response(serializer.data)

    # post请求添加数据
    # 使用这个之后就会呈现一个post入口
    def post(self, request):
        data = request.data
        serializer = MenuSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # print(serializer.data['id'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MenuDetail(APIView):
    queryset = Menu.objects.all()
    authentication_classes = [TokenAuth, ]
    permission_classes = [DjangoModelPermissions, ]
    def get_object(self, pk):
        try:
            return Menu.objects.get(pk=pk)
        except Exception as e:
            pass

    #http://localhost:8000/menu/menudetail/2/
    def get(self, request, pk):
        # print(request.user)
        menu = self.get_object(pk)
        serializer = MenuSerializer(menu)
        return Response(serializer.data)

    def put(self, request, pk):
        menu = self.get_object(pk)
        serializer = MenuSerializer(menu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        menu = self.get_object(pk)
        menuChildren = Menu.objects.filter(parentId=menu.id)
        if menu.is_parent and menuChildren.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            menu.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


