# -*- coding: utf-8 -*-
# @Time    : 2019/1/7 16:58
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : getDataUtils.py
# @Software: PyCharm
from .models import Contract
import datetime
import time
from django.core.cache import cache
from django.db.models import Q
from .constantUtils import ConstantUtil
from .models import YishengUser, UserSites
from .BusinessUtils import BusinessUtils
#判断用户是否为vip，判定规则为：广告到期时间 - 现在时间 大于 0。
def getContractInfoByUseName(user_id, _dict):
    '''
    :param user_id: 易数宝用户id
    :param _dict:  返回的字典
    :return:
    '''
    contract = Contract.objects.filter(user_id_back=user_id).order_by('-ad_offline_date').first()
    if contract:
        startDate = contract.ad_online_date
        endDate = contract.ad_offline_date
        currentDate = str(datetime.datetime.now().year) + '-' + str(datetime.datetime.now().month) + '-' + str(datetime.datetime.now().day)
        if startDate and endDate:
            _endDate = str(str(endDate).split(' ')[0])
            daySub = Caltime(str(currentDate), str(_endDate))
            if daySub > 0:
                _dict['ad_online_date'] = startDate
                _dict['ad_offline_data'] = endDate
                _dict['is_vip'] = str(1)
            else:
                _dict['ad_online_date'] = startDate
                _dict['ad_offline_data'] = endDate
                _dict['is_vip'] = str(0)
        else:
            if endDate is None:
                _dict['ad_online_date'] = startDate
                _dict['ad_offline_data'] = endDate
                _dict['is_vip'] = str(1)

    return _dict




#计算两个日期相差天数，自定义函数名，和两个日期的变量名。
def Caltime(date1, date2):
    date1 = time.strptime(date1, "%Y-%m-%d")
    date2 = time.strptime(date2, "%Y-%m-%d")
    date1 = datetime.datetime(date1[0], date1[1], date1[2])
    date2 = datetime.datetime(date2[0], date2[1], date2[2])
    #返回两个变量相差的值，就是相差天数
    subDay = date2 - date1
    return subDay.days

#用户重新登录时移除原有的缓存
def removeTokenCache(username):
    '''
    查看缓存用户信息字典中key为‘username'的value是否传来的username, 是则将缓存清除
    :param username:
    :return:
    '''
    keys_list = cache.keys(ConstantUtil.TOKEN_KEY_PRE+'*')
    for key in keys_list:
        user_json = cache.get(key)
        if 'username' in user_json and username == user_json['username']:
            cache.delete(key)

#通过token获取用户信息
def getUserInfoByToken(token):
    '''
    :param token: app端传来的yisheng_token
    :return:
    '''
    real_token = ConstantUtil.TOKEN_KEY_PRE+token
    if token:
        if cache.has_key(real_token):
            user_info = cache.get(real_token)
            return user_info
        else:
            return None
    else:
        return None

#检查旧密码是否正确
def checkPassword(userId, password_old):
    '''
    :param userId: 易数宝用户id
    :param password_old: 易数宝用户旧密码
    :return:
    '''
    users = YishengUser.objects.filter(id=userId, password=password_old)
    if users:
        return True
    else:
        return False

#修改，检查域名的唯一性 存在返回true，不存在返回false为（false才能提交)
def doCheckDomainExistUpdate(userId, domain, siteid):
    '''
    :param userId: 易数宝用户id
    :param domain: 易数宝注册域名
    :param siteid: 域名id
    :return:
    '''
    b = BusinessUtils()
    domain = b.urlFilter(b.wwwFilter(domain))
    userSite_01 = UserSites.objects.filter(user_id=userId, domain=domain).first()
    userSite_02 = UserSites.objects.filter(~Q(user_id=userId), domain=domain).first()
    if userSite_01:
        if siteid == userSite_01.id:
            return False
        else:
            return True
    else:
        if userSite_02:
            return True
        else:
            return False
#新增，检查域名的唯一性，存在返回true，不存在返回false
def checkDomainExistAdd(domain):
    '''
    :param domain: 用户输入的新域名
    :return:
    '''
    b = BusinessUtils()
    domain = b.urlFilter(b.wwwFilter(domain))
    us = UserSites.objects.filter(domain=domain).first()
    if us:
        return True
    else:
        return False

