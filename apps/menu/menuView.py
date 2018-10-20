# -*- coding: utf-8 -*-
# @Time    : 2018/10/12 17:04
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : menuView.py
# @Software: PyCharm
from django.views.decorators.csrf import csrf_exempt
from menu.models import Menu
from django.http import JsonResponse
import json
from systemToken.models import SystemToken
from utils.jsonTreeUtils import initJsonTree
from django.db.models import Q
from utils.apiAuth import TokenAuth
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.views import APIView
class initMenuTreeAPIView(APIView):
    queryset = Menu.objects.all()
    authentication_classes = [TokenAuth, ]
    permission_classes = [DjangoModelPermissions, ]
    def get(self, request):
        response = {}
        menus = Menu.objects.all()
        ret = initJsonTree(menus)
        response['message'] = ret
        response['code'] = 200
        return JsonResponse(response)


@csrf_exempt
def checkMenuCode(request):
    response = {}
    menuCode = request.GET.get('menuCode')
    menuId = request.GET.get('menuId')
    r = None
    if not menuId is None:
        r = Menu.objects.filter(~Q(id=menuId), menuCode=menuCode)
    else:
        r = Menu.objects.filter(menuCode=menuCode)
    if r.exists():
        response['message'] = '该编码已占用'
        response['code'] = 300
    else:
        response['message'] = '该编码可用'
        response['code'] = 200
    return JsonResponse(response)


@csrf_exempt
def oneKeyToAddMenu(requset):
   if requset.method == 'POST':
       result = {}
       result['code'] = 200
       data = requset.body
       str_data = str(data, encoding='utf-8')
       json_data = json.loads(str_data)
       for menu in json_data:
           handleAddMenu(menu)


       return JsonResponse(result)


def handleAddMenu(menu):
    name = menu['name']
    path = menu['path']
    menuCode = menu['menuCode']
    is_parent = menu['is_parent']
    exist_menu = Menu.objects.filter(menuCode=menuCode)
    iconCls = None
    if 'iconCls' in menu:
        iconCls = menu['iconCls']
    if exist_menu.exists():
        up_menu = exist_menu.first()
        if is_parent:
            Menu.objects.filter(id=up_menu.id).update(name=name, is_parent=is_parent, path=path, iconCls=iconCls, menuCode=menuCode)
        else:
            if 'parent_code' in menu:
                parent_code = menu['parent_code']
                if not parent_code is None:
                    m = Menu.objects.filter(menuCode=parent_code).first()
                    if not m is None:
                        Menu.objects.filter(id=up_menu.id).update(name=name, is_parent=is_parent, path=path, iconCls=iconCls, menuCode=menuCode, parentId=m.id)
    else:
        if is_parent:
            Menu.objects.create(name=name, is_parent=is_parent, path=path, iconCls=iconCls, menuCode=menuCode)
        else:
            if 'parent_code' in menu:
                parent_code = menu['parent_code']
                if not parent_code is None:
                    m = Menu.objects.filter(menuCode=parent_code).first()
                    if not m is None:
                        Menu.objects.create(name=name, is_parent=is_parent, path=path, iconCls=iconCls, menuCode=menuCode, parentId=m.id)
    if 'children' in menu:
        m_ch = menu['children']
        for jd in m_ch:
            handleAddMenu(jd)


