# -*- coding: utf-8 -*-
# @Time    : 2018/12/29 16:41
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : YunPian.py
# @Software: PyCharm
import requests
import json

def send_sms(mobile, template_type):
    params = {'phone_number': mobile, 'sign_name': '原昇科技', 'template_code': 'SMS_143860075', 'template_type': template_type}
    single_send_url = 'http://service.beebos.nisure.cn/admin/templeteRequest'
    response = requests.post(single_send_url, data=params)
    re_dict = json.loads(response.text)
    return re_dict

if __name__ == '__main__':
    print(send_sms('18819470279', '1'))
