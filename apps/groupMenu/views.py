from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from systemToken.models import SystemToken
from django.http import JsonResponse
from users.models import UserProfile
from menu.models import Menu
from groupMenu.models import GroupMenu
from django.contrib.auth.models import Group
@csrf_exempt
def getRoleMenuList(request):
    response = {}
    result_data = None
    role_name = None
    http_token = request.META.get("HTTP_AUTHORIZATION")
    st = SystemToken.objects.filter(token=http_token).first()
    if not st is None:
        user_id = st.user_id
        up = UserProfile.objects.get(id=user_id)
        if up.is_superuser:
            menus = Menu.objects.all()
            role_name = 'superUser'
            if menus.exists():
                result_data = initJsonMenuTree(menus)

        else:
            ur = Group.objects.filter(user=up).first()
            role_name = 'normalUser'
            if not ur is None:
                rm = GroupMenu.objects.filter(group=ur)
                if rm.exists():
                    menu_id_list = []
                    for r in rm:
                        menu_id_list.append(r.menu.id)
                    oMenus = Menu.objects.filter(id__in=menu_id_list)
                    result_data = initJsonMenuTree(oMenus)

    response['MenuCodeList'] = result_data
    response['MenuRoleName'] = role_name
    return JsonResponse(response)


from django.forms.models import model_to_dict
def initJsonMenuTree(queryset_modle):
    list_modle = []
    ret = []
    if queryset_modle.exists():
        for modle in queryset_modle:
            modle_dict = model_to_dict(modle)
            m = Menu.objects.filter(parentId=modle_dict['id'])
            if m.exists():
                modle_dict['children'] = []
            list_modle.append(modle_dict)
    list_dict = {}
    if list_modle:
        for m in list_modle:
            list_dict[m['id']] = m
        for men in list_modle:
            parentId = men['parentId']
            if not parentId is None and parentId != '':
                list_dict[parentId]['children'].append(men)
            else:
                ret.append(men)
    return ret
