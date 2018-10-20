from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from systemToken.models import SystemToken
from users.models import UserProfile
from django.contrib.auth.models import Group
@csrf_exempt
def getUserOwnRole(request):
    response = {}
    http_token = request.META.get("HTTP_AUTHORIZATION")
    checkUserId = request.GET.get('checkUserId')
    token_obj = SystemToken.objects.filter(token=http_token).first()
    # 验证失败
    if not token_obj:
        response['roleId'] = None
        return JsonResponse(response)
    else:
        ur = UserProfile.objects.get(id=checkUserId)
        group_set = Group.objects.filter(user=ur).first()
        if not group_set is None:
            response['roleId'] = group_set.id
        else:
            response['roleId'] = None
        return JsonResponse(response)
