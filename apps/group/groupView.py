# -*- coding: utf-8 -*-
# @Time    : 2018/10/10 10:00
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : groupView.py
# @Software: PyCharm
from django.views.decorators.csrf import csrf_exempt
import json
from systemToken.models import SystemToken
from django.http import JsonResponse
from depart.models import Depart
from menu.models import Menu
from groupMenu.models import GroupMenu
from groupDepart.models import GroupDepart
from django.db.models import Q
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
@csrf_exempt
def getAllRoles(request):
    response = {}
    http_token = request.META.get("HTTP_AUTHORIZATION")
    token_obj = SystemToken.objects.filter(token=http_token).first()
    # 验证失败
    if not token_obj:
        return JsonResponse(response)
    result_set = Group.objects.all().values('id', 'name')
    result_json = json.dumps(list(result_set))
    response['roleJson'] = result_json
    return JsonResponse(response)


@csrf_exempt
# @require_http_methods(["GET",'POST'])
def initRoleEditValue(request):
    response = {}
    http_token = request.META.get("HTTP_AUTHORIZATION")
    roleId = request.GET.get('queryRoleId')
    token_obj = SystemToken.objects.filter(token=http_token).first()
    rolePermissions = []
    # 验证失败
    if not token_obj:
        return JsonResponse(response)
    if not roleId is None:
        rd = GroupDepart.objects.filter(group_id=roleId).first()
        if not rd is None:
            response['departKey'] = rd.depart.id
            response['departName'] = rd.depart.name
        role_menu = []
        rm = GroupMenu.objects.filter(group_id=roleId)
        if rm.exists():
            for r in rm:
                m = Menu.objects.get(id=r.menu.id)
                if not m is None:
                    if m.is_parent == False:
                        role_menu.append(r.menu.id)
        response['menuKey'] = role_menu
        group = Group.objects.get(id=roleId)
        permissionIds = Permission.objects.filter(group=group)
        if permissionIds.exists():
            for permissionId in permissionIds:
                rolePermissions.append(permissionId.id)
        response['rolePermissions'] = rolePermissions
        return JsonResponse(response)
    else:
        return JsonResponse(response)

@csrf_exempt
def roleFormatterValue(request):
    response = {}
    http_token = request.META.get("HTTP_AUTHORIZATION")
    roleId = request.GET.get('queryRoleId')
    token_obj = SystemToken.objects.filter(token=http_token).first()
    # 验证失败
    if not token_obj:
        return JsonResponse(response)
    rd = GroupDepart.objects.filter(group_id=roleId).first()
    if not rd is None:
        d = Depart.objects.get(id=rd.depart.id)
        if not d is None:
            response['departName'] = d.name
        else:
            response['departName'] = '未选择部门'

    else:
        response['departName'] = '未选择部门'
    return JsonResponse(response)

@csrf_exempt
def checkRoleName(request):
    response = {}
    roleName = request.GET.get('roleName')
    roleId = request.GET.get('roleId')
    r = None
    if not roleId is None:
        r = Group.objects.filter(~Q(id=roleId), name=roleName)
    else:
        r = Group.objects.filter(name=roleName)
    if r.exists():
        response['message'] = '角色名已占用'
        response['code'] = 300
    else:
        response['message'] = '角色名可用'
        response['code'] = 200
    return JsonResponse(response)
