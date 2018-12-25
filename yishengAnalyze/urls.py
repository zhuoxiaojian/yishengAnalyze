"""yishengAnalyze URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.generic import RedirectView
import xadmin
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token
urlpatterns = [
    url('^admin/', xadmin.site.urls),
    # url('^$', RedirectView.as_view(url='/admin'), name='login'),
    url('^login/', RedirectView.as_view(url='/admin'), name='login'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^appfront/', TemplateView.as_view(template_name="index.html")),
    url(r'^api/token', obtain_auth_token, name='api_token'),

    # 系统管理API
    url(r'^menu/', include('menu.urls')),
    url(r'^user/', include('users.urls')),
    url(r'^role/', include('group.urls')),
    url(r'^depart/', include('depart.urls')),
    url(r'^roleMenu/', include('groupMenu.urls')),
    url(r'^userRole/', include('group.urls')),
    url(r'^constant/', include('constant.urls')),
    url(r'^permissions/', include('permission.urls')),
    url(r'^contentType/', include('contentType.urls')),
    #
    url(r'^api/v1/login/$', obtain_jwt_token, name='APILogin'),
    url(r'^yiShengUser/', include('yiShengUser.urls'))
]
