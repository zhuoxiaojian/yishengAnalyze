from django.shortcuts import render

# Create your views here.
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from users.models import UserProfile
#自定义用户认证方法
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 全局 404 处理函数
def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


# 全局 500 处理函数
def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response



