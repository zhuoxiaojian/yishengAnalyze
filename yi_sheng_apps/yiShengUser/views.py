from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from yiShengUser.models import YiShengUser
from django.http import JsonResponse
from users.models import UserProfile
from django.core import serializers
@csrf_exempt
def test(request):
    u = UserProfile.objects.all()
    y = YiShengUser.objects.all()
    return JsonResponse({"system_user": serializers.serialize('json', u), "yishubao_user": serializers.serialize('json', y)})
