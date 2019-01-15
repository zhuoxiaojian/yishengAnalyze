# -*- coding: utf-8 -*-
# @Time    : 2019/1/7 11:46
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : AppRemoteApiViews.py
# @Software: PyCharm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .AppRemoteApiAuth import api_auth
from .constantUtils import ConstantUtil
import re
from .BeeBos import send_sms
from base64 import b64encode
from utils.MakeToken import get_token_code
from .models import YishengUser, UserSites, VerifyCode
from django.forms.models import model_to_dict
import datetime
from django.core.cache import cache
from .constantUtils import ConstantUtil
from . import getDataUtils
from .verifyUtils import Captcha
from django.db import transaction
@csrf_exempt
@api_auth
def testData(request):
    if request.method == 'POST':
        print(request.POST)
        print(request.POST._mutable)
        return JsonResponse({'message': 'success', 'dict': request.POST.dict()})
    elif request.method == 'GET':
        print(request.GET)
        print(request.GET._mutable)
        return JsonResponse({'message': 'success', 'dict': request.GET.dict()})
#app端获取图形验证码
def randCodeImage(request):
    captcha = Captcha()
    tk, im_buf = captcha.captcha()
    # return HttpResponse(im_buf, content_type='image/png')
    # var captchaImg = response.data.captcha;
    # document.getElementById('verifyImg').setAttribute('src','data:image/png;base64,'+captchaImg);
    response = {'recode': 1,
                'remsg': '获取成功！',
                'data': {'timestamp': tk, 'captcha': b64encode(im_buf.read()).decode('utf-8')}}
    return JsonResponse(response)


#app端获取 注册/登录 验证码
@csrf_exempt
def sendSms(request):
    response = {}
    mobile = None
    template_type = None
    appSource = None
    method = request.method
    if method == 'POST':
        mobile = request.POST.get('mobile')
        template_type = request.POST.get('type')
        appSource = request.POST.get('appSource')
    elif method == 'GET':
        mobile = request.GET.get('mobile')
        template_type = request.GET.get('type')
        appSource = request.GET.get('appSource')
    response['mobile'] = mobile
    response['method'] = method
    if appSource and template_type and mobile:
        response = handleSmsCode(response, mobile, template_type, appSource)
    else:
        response['message'] = '信息不完整'
    return JsonResponse(response)

def handleSmsCode(response, mobile, template_type, appSource):
    '''
    :param response: 返回的json串
    :param mobile: 手机号/用户名
    :param template_type: 对应阿里云的短信注册模板
    :param appSource: 区分应用来源（易数宝/汇桔宝)
    :return:
    '''
    if not re.match(ConstantUtil.REGEX_MOBILE, mobile):
        response['message'] = '手机号格式错误'
    else:
        try:
            users = YishengUser.objects.filter(username=mobile).first()
            if ConstantUtil.APP_YSB == appSource and template_type == ConstantUtil.YSB_REGISTRY:
                if users:
                    response['message'] = '用户已注册'
                else:
                    response = handleSendMsg(response, mobile, template_type, ConstantUtil.REGISTRY_CODE_TYPE)

            elif ConstantUtil.APP_YSB == appSource and template_type == ConstantUtil.YSB_LOGIN:
                if users:
                    response = handleSendMsg(response, mobile, template_type, ConstantUtil.LOGIN_CODE_TYPE)
                else:
                    response['message'] = '用户未注册'

            elif ConstantUtil.APP_HJB == appSource and template_type == ConstantUtil.HJB_REGISTRY:
                if users:
                    response['message'] = '用户已注册'
                else:
                    response = handleSendMsg(response, mobile, template_type, ConstantUtil.REGISTRY_CODE_TYPE)

            elif ConstantUtil.APP_HJB == appSource and template_type == ConstantUtil.HJB_LOGIN:
                if users:
                    response = handleSendMsg(response, mobile, template_type, ConstantUtil.LOGIN_CODE_TYPE)
                else:
                    response['message'] = '用户未注册'
        except Exception as e:
            print(e)
            response['message'] = '验证码发送失败'
    return response

def handleSendMsg(response, mobile, template_type, code_type):
    '''
    :param response: 返回的json串
    :param mobile: 手机号/用户名
    :param template_type: 对应阿里云的短信注册模板
    :param code_type: 对应验证码表中获取验证码的类型（注册/登录)
    :return:
    '''
    one_minute_age = datetime.datetime.now() - datetime.timedelta(hours=0, minutes=1, seconds=0)
    if VerifyCode.objects.filter(add_time__gt=one_minute_age, mobile=mobile, code_type=code_type).count():
        response['message'] = '请一分钟后再次发送'
    else:
        try:
            code_json = send_sms(mobile, template_type)
            message = code_json['Message']
            code = None
            if "OK" == message:
                code = code_json['RandomCode']
            vc = VerifyCode.objects.filter(mobile=mobile, code_type=code_type)
            if vc.exists():
                VerifyCode.objects.filter(mobile=mobile, code_type=code_type).update(code=code, add_time=datetime.datetime.now())
            else:
                VerifyCode.objects.create(mobile=mobile, code_type=code_type, add_time=datetime.datetime.now(), code=code)
            response['message'] = '验证码已发送'
        except Exception as e:
            print(e)
            response['message'] = '验证码发送失败'
    return response



#app端注册用户
@csrf_exempt
def doMsgRegistry(request):
    response = {}
    username = None
    password = None
    smscode = None
    appSource = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        smscode = request.POST.get('smscode')
        appSource = request.POST.get('appSource')
    elif request.method == 'GET':
        username = request.GET.get('username')
        password = request.GET.get('password')
        smscode = request.GET.get('smscode')
        appSource = request.GET.get('appSource')

    if username and password and smscode and appSource:
        username = username.strip()
        password = password.strip()
        yu = YishengUser.objects.filter(username=username).first()
        if not yu:
            verify_records = VerifyCode.objects.filter(mobile=username, code_type=ConstantUtil.REGISTRY_CODE_TYPE, code=smscode).order_by('-add_time')
            if verify_records:
                last_record = verify_records[0]
                # 判断验证码是否过期
                five_minutes_ago = datetime.datetime.now() - datetime.timedelta(hours=0, minutes=2, seconds=0)  # 获取5分钟之前的时间
                if last_record.add_time < five_minutes_ago:
                    response['message'] = '验证码已过期'
                else:
                    YishengUser.objects.create(username=username, password=password, mobile=username, create_name='客户',
                                               role_id='normal', company_name='公司名称未填写', email='', address='',
                                               postcode='', user_status=0, app_source=appSource
                                               )
                    response['message'] = '用户注册成功'
            else:
                response['message'] = '手机或验证码验证码错误'
        else:
            response['message'] = '用户已注册'
    else:
        response['message'] = '信息不完整'
    return JsonResponse(response)

#app端验证码登录
@csrf_exempt
def smslogin(request):
    response = {}
    username = None
    smscode = None
    if request.method == 'POST':
        username = request.POST.get('username')
        smscode = request.POST.get('smscode')
    elif request.method == 'GET':
        username = request.GET.get('username')
        smscode = request.GET.get('smscode')
    if username and smscode:
        users = YishengUser.objects.filter(username=username).first()
        verify_records = VerifyCode.objects.filter(mobile=username, code_type=ConstantUtil.LOGIN_CODE_TYPE, code=smscode).order_by('-add_time')
        if users and verify_records:
            last_record = verify_records[0]
            # 判断验证码是否过期
            five_minutes_ago = datetime.datetime.now() - datetime.timedelta(hours=0, minutes=2, seconds=0)  # 获取5分钟之前的时间
            if last_record.add_time < five_minutes_ago:
                response['message'] = '验证码已过期'
                response['success'] = False
            else:
                yisheng_token = get_token_code(username)
                companyName = users.company_name
                user_id = users.id
                email = users.email
                mobile = users.mobile
                address = users.address
                postcode = users.postcode
                idnumber = users.idnumber
                userStatus = users.user_status
                role = users.role_id
                ip = None
                if 'HTTP_X_FORWARDED_FOR' in request.META:
                    ip = request.META['HTTP_X_FORWARDED_FOR']
                else:
                    ip = request.META['REMOTE_ADDR']
                user_info = {}
                user_info['yisheng_token'] = yisheng_token
                user_info['companyName'] = companyName
                user_info['email'] = email
                user_info['mobile'] = mobile
                user_info['address'] = address
                user_info['postcode'] = postcode
                user_info['idnumber'] = idnumber
                user_info['userStatus'] = userStatus
                user_info['role'] = role
                user_info['username'] = username
                user_info['timeout_server'] = 606600
                user_info['ip'] = ip
                user_info['loginTime'] = datetime.datetime.now()
                us = UserSites.objects.filter(user_id=user_id)
                if us.exists():
                    user_info['siteKey'] = us[0].id
                    user_info['industrykey'] = us[0].industry_id

                user_info = getDataUtils.getContractInfoByUseName(user_id, user_info)
                cache_info = model_to_dict(users)
                cache_info['id'] = user_id
                getDataUtils.removeTokenCache(username)
                cache.set(ConstantUtil.TOKEN_KEY_PRE+str(yisheng_token), cache_info, ConstantUtil.LOGIN_INFO_EXPIRE)
                response['message'] = '登录成功'
                response['success'] = True
                response = dict(response, **user_info)
        else:
            response['message'] = '手机号或验证码错误'
            response['success'] = False
    else:
        response['message'] = '信息不完整'
        response['success'] = False

    return JsonResponse(response)

#app端普通登录
@csrf_exempt
def login(request):
    response = {}
    username = None
    password = None
    randCode = None
    randCodeId = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        randCode = request.POST.get('randCode')
        randCodeId = request.POST.get('randCodeId')
    elif request.method == 'GET':
        username = request.GET.get('username')
        password = request.GET.get('password')
        randCode = request.GET.get('randCode')
        randCodeId = request.GET.get('randCodeId')
    if username and password and randCode and randCodeId:
        users = YishengUser.objects.filter(username=username, password=password).first()
        if users:
            randCodeId = str(randCodeId)
            captcha = Captcha()
            flag = captcha.verify_captcha(randCodeId, randCode)
            if not flag:
                response['message'] = '验证码错误'
                response['success'] = False
                return JsonResponse(response)
            yisheng_token = get_token_code(username)
            companyName = users.company_name
            user_id = users.id
            email = users.email
            mobile = users.mobile
            address = users.address
            postcode = users.postcode
            idnumber = users.idnumber
            userStatus = users.user_status
            role = users.role_id
            ip = None
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                ip = request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = request.META['REMOTE_ADDR']
            user_info = {}
            user_info['yisheng_token'] = yisheng_token
            user_info['companyName'] = companyName
            user_info['email'] = email
            user_info['mobile'] = mobile
            user_info['address'] = address
            user_info['postcode'] = postcode
            user_info['idnumber'] = idnumber
            user_info['userStatus'] = userStatus
            user_info['role'] = role
            user_info['username'] = username
            user_info['timeout_server'] = 606600
            user_info['ip'] = ip
            user_info['loginTime'] = datetime.datetime.now()
            us = UserSites.objects.filter(user_id=user_id)
            if us.exists():
                user_info['siteKey'] = us[0].id
                user_info['industrykey'] = us[0].industry_id

            user_info = getDataUtils.getContractInfoByUseName(user_id, user_info)
            cache_info = model_to_dict(users)
            cache_info['id'] = user_id
            getDataUtils.removeTokenCache(username)
            cache.set(ConstantUtil.TOKEN_KEY_PRE+str(yisheng_token), cache_info, ConstantUtil.LOGIN_INFO_EXPIRE)
            response['message'] = '登录成功'
            response['success'] = True
            response = dict(response, **user_info)
        else:
            response['message'] = '手机号或密码错误'
            response['success'] = False
    else:
        response['message'] = '信息不完整'
        response['success'] = False

    return JsonResponse(response)


#修改用户密码
@csrf_exempt
@api_auth
def updatePasword(request):
    #yisheng_token=&password_old=yishengtest&password_new=yishengtest123
    response = {}
    user_id = None
    password_old = None
    password_new = None
    if request.method == 'POST':
        user_id = request.POST.get('userId')
        password_old = request.POST.get('password_old')
        password_new = request.POST.get('password_new')
    elif request.method == 'GET':
        user_id = request.GET.get('userId')
        password_old = request.GET.get('password_old')
        password_new = request.GET.get('password_new')

    if not password_old:
        response['message'] = 'parameter_null'
        response['success'] = False
        return JsonResponse(response)
    else:
        if getDataUtils.checkPassword(user_id, password_old):
            if password_old == password_new:
                response['message'] = 'new password cannot be same with new password'
                response['success'] = False
                return JsonResponse(response)
            elif password_new:
                YishengUser.objects.filter(id=user_id).update(password=password_new)
                response['message'] = 'updatePwd_success'
                response['success'] = True
                return JsonResponse(response)
            else:
                response['message'] = 'new password cannot be empty'
                response['success'] = False
                return JsonResponse(response)
        else:
            response['message'] = 'oldPassword_error'
            response['success'] = False
            return JsonResponse(response)

#查询用户全部信息
@csrf_exempt
@api_auth
def listUser(request):
    response = {}
    userId = None
    if request.method == 'POST':
        userId = request.POST.get('userId')
    elif request.method == 'GET':
        userId = request.GET.get('userId')
    if userId:
        try:
            user = YishengUser.objects.get(id=userId)
            response = model_to_dict(user)
            return JsonResponse(response)
        except YishengUser.DoesNotExist:
            return JsonResponse(response)
    else:
        return JsonResponse(response)

#提交修改的用户信息
@csrf_exempt
@api_auth
def doUpdate(request):
    response = {}
    userId = None
    query_dict = None
    if request.method == 'POST':
        userId = request.POST.get('userId')
        query_dict = request.POST
    elif request.method == 'GET':
        userId = request.GET.get('userId')
        query_dict = request.GET
    if userId and query_dict:
        try:
            with transaction.atomic():
                user = YishengUser.objects.get(id=userId)
                user_dict = query_dict.dict()
                for item in user_dict:
                    if user_dict[item]:
                        setattr(user, item, user_dict[item])
                user.save()
            response['message'] = 'user update success'
        except YishengUser.DoesNotExist:
            response['message'] = 'user update fail'

    return JsonResponse(response)

#修改，检查域名的唯一性 存在返回true，不存在返回false为（false才能提交)
@csrf_exempt
@api_auth
def doCheckDomainExistUpdate(request):
    response = {}
    domain = None
    siteId = None
    userId = None
    if request.method == 'POST':
        domain = request.POST.get('domain')
        siteId = request.POST.get('siteId')
        userId = request.POST.get('userId')
    elif request.method == 'GET':
        domain = request.GET.get('domain')
        siteId = request.GET.get('siteId')
        userId = request.GET.get('userId')
    if userId and domain and siteId:
        if getDataUtils.doCheckDomainExistUpdate(userId, domain, siteId):
            response['message'] = 'domain_Exist'
            response['success'] = True
        else:
            response['message'] = 'domain_NoExist'
            response['success'] = False
    else:
        response['message'] = 'parameter_null'
        response['success'] = True

    return JsonResponse(response)
#添加网站, 检查域名唯一性
@csrf_exempt
@api_auth
def doCheckDomainExistAdd(request):
    response = {}
    domain = None
    if request.method == 'POST':
        domain = request.POST.get('domain')
    elif request.method == 'GET':
        domain = request.GET.get('domain')
    if domain:
        if getDataUtils.checkDomainExistAdd(domain):
            response['message'] = 'domain_Exist'
            response['success'] = True
        else:
            response['message'] = 'domain_NoExist'
            response['success'] = False
    else:
        response['message'] = 'parameter_null'
        response['success'] = True
    return JsonResponse(response)

#添加网站和ftp信息
@csrf_exempt
def doAddSitesFtp(request):
    u = YishengUser()
    query_dict = request.GET.dict()
    for item in query_dict:
        setattr(u, item, query_dict[item])
    print(u)
    return JsonResponse({'message': model_to_dict(u)})
