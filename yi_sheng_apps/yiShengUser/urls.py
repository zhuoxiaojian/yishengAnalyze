# -*- coding: utf-8 -*-
# @Time    : 2018/10/22 14:23
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : urls.py
# @Software: PyCharm
from django.conf.urls import url
from . import views, yiShengUserAPIViews
from .SmsCodeViewSet import SmsRegistryCodeViewSet, SmsLoginCodeViewSet
from .YiShengUserViewset import UserRegisterViewset, UserLoginViewset, UserSmsLoginViewset
from . import AppRemoteApiViews
urlpatterns = [
    url(r'^test/$', views.test, name='test'),
    url(r'getcompanyInfoById/$', views.getcompanyInfoById, name='getcompanyInfoById'),
    url(r'getAllBaiduAccount/$', views.getAllBaiduAccount, name='getAllBaiduAccount'),
    url(r'^getVerify/$', views.get_verify_img, name='getVerify'),
    url(r'^checkVerify/$', views.check_verify_img, name='checkVerify'),
    url(r'^yiShengUser/', yiShengUserAPIViews.YiShengUserApiView.as_view()),
    url(r'^yiShengUserDetail/', yiShengUserAPIViews.YiShengUserDetail.as_view()),
    url(r'^getRegistryCode/$', SmsRegistryCodeViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    url(r'^getLoginCode/$', SmsLoginCodeViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    url(r'^registerUser/$', UserRegisterViewset.as_view({
        'get': 'list',
        'post': 'create',
    })),
    url(r'^loginUser/$', UserLoginViewset.as_view({
        'get': 'list',
        'post': 'create',
    })),
    url(r'^smsLoginUser/$', UserSmsLoginViewset.as_view({
        'get': 'list',
        'post': 'create',
    })),
    #测试自定义api_auth
    url(r'^testData/$', AppRemoteApiViews.testData, name='testData'),
    url(r'^randCodeImage/$', AppRemoteApiViews.randCodeImage, name='randCodeImage'),
    url(r'^doMsgRegistry/$', AppRemoteApiViews.doMsgRegistry, name='doMsgRegistry'),
    url(r'^smslogin/$', AppRemoteApiViews.smslogin, name='smslogin'),
    url(r'^login/$', AppRemoteApiViews.login, name='login'),
    url(r'^sendSms/$', AppRemoteApiViews.sendSms, name='sendSms'),
    url(r'^updatePasword/$', AppRemoteApiViews.updatePasword, name='updatePasword'),
    url(r'^listUser/$', AppRemoteApiViews.listUser, name='listUser'),
    url(r'^doUpdate/$', AppRemoteApiViews.doUpdate, name='doUpdate'),
    url(r'^doCheckDomainExistUpdate/$', AppRemoteApiViews.doCheckDomainExistUpdate, name='doCheckDomainExistUpdate'),
    url(r'^doCheckDomainExistAdd/$', AppRemoteApiViews.doCheckDomainExistAdd, name='doCheckDomainExistAdd'),
    url(r'^doAddSitesFtp/$', AppRemoteApiViews.doAddSitesFtp, name='doAddSitesFtp')

    ]

'''
from snippets import views
from rest_framework.routers import DefaultRouter.
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)
url(r'^', include(router.urls)),
'''