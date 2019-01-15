
from .verifyUtils import Captcha
from base64 import b64encode
from django.views.decorators.csrf import csrf_exempt
from yiShengUser.models import YishengUser
from django.http import JsonResponse, HttpResponse
from users.models import UserProfile
from django.core import serializers
@csrf_exempt
def test(request):
    u = UserProfile.objects.all()
    y = YishengUser.objects.all()
    return JsonResponse({"system_user": serializers.serialize('json', u), "yishubao_user": serializers.serialize('json', y)})



@csrf_exempt
def get_verify_img(request):
    captcha = Captcha()
    tk, im_buf = captcha.captcha()
    # return HttpResponse(im_buf, content_type='image/png')

    # var captchaImg = response.data.captcha;
    # document.getElementById('verifyImg').setAttribute('src','data:image/png;base64,'+captchaImg);
    response = {'recode': 1,
                'remsg': '获取成功！',
                'data': {'timestamp': tk, 'captcha': b64encode(im_buf.read()).decode('utf-8')}}
    return JsonResponse(response)

@csrf_exempt
def check_verify_img(request):
    if request.method == "POST":
        key = request.POST.get('verifyID')
        value = request.POST.get('verifyCode')
        captcha = Captcha()
        flag = captcha.verify_captcha(key, value)
        if flag:
            return JsonResponse({'code': 200, 'message': '验证码正确'})
        else:
            return JsonResponse({'code': 201, 'message': '验证码错误'})

    return JsonResponse({'code': 200})

#测试接口
@csrf_exempt
def getcompanyInfoById(request):
    companyId = request.GET.get('companyId')
    #from django.db import connection
    #cursor = connection.cursor()
    from django.db import connections
    cursor = connections['db01'].cursor()
    sql = "SELECT yu.id,yu.company_name,yhpu.company_id,yhpu.login_name,yhpu.login_password,yhpu.token,yu.user_id_KAD \
    FROM yisheng_hitavg_price_user yhpu, yisheng_user yu where yu.id='"+ companyId + "' \
    and yhpu.token!='null' and yhpu.token!='' and yu.company_id=yhpu.company_id LIMIT 1"
    cursor.execute(sql)
    rows = cursor.fetchall() #读取所有
    result_dict = {}
    if rows:
        row = rows[0]
        result_dict['id'] = row[0]
        result_dict['company_name'] = row[1]
        result_dict['company_id'] = row[2]
        result_dict['login_name'] = row[3]
        result_dict['login_password'] = row[4]
        result_dict['token'] = row[5]
        result_dict['user_id_KAD'] = row[6]
    cursor.close()
    return JsonResponse(result_dict)

@csrf_exempt
def getAllBaiduAccount(request):
    from django.db import connections
    response = {}
    result_list = []
    cursor = connections['db01'].cursor()
    sbSql = "SELECT yhpu.id, yu.company_id, yu.company_name,yhpu.login_name,yhpu.login_password,yhpu.token, \
    yu.user_id_KAD,yu.phone_pay \
    FROM yisheng_hitavg_price_user yhpu, yisheng_user yu \
    where yu.pay_status in('0','1') and yu.company_id=yhpu.company_id and yhpu.token \
    IS NOT NULL and yhpu.token != '' AND yhpu.token != 'null'"
    cursor.execute(sbSql)
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            result_dict = {}
            result_dict['id'] = row[0]
            result_dict['company_id'] = row[1]
            result_dict['company_name'] = row[2]
            result_dict['login_name'] = row[3]
            result_dict['login_password'] = row[4]
            result_dict['token'] = row[5]
            result_dict['user_id_KAD'] = row[6]
            result_dict['phone_pay'] = row[7]
            result_list.append(result_dict)
    response['count'] = len(result_list)
    response['result'] = result_list
    cursor.close()
    return JsonResponse(response)




