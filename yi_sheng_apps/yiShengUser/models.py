from django.db import models
import datetime
import uuid

class VerifyCode(models.Model):
    mobile = models.CharField(verbose_name='手机号', max_length=255, null=False, blank=False, db_index=True)
    code = models.CharField(verbose_name='验证码', max_length=255, null=False, blank=False)
    add_time = models.DateTimeField(verbose_name='发送时间', null=False, blank=False, default=datetime.datetime.now)
    code_type = models.CharField(verbose_name='验证码类型', max_length=255, null=False, blank=False, db_index=True)

    class Meta:
        app_label = 'verifyCode'
        db_table = 'ys_verify_code'
        verbose_name = '验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.mobile


class Channel(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid1().hex, max_length=36, editable=False, verbose_name='ID')
    create_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='创建人名称')
    create_by = models.CharField(max_length=50, blank=True, null=True, verbose_name='创建人登录名称')
    create_date = models.DateTimeField(blank=True, null=True, verbose_name='创建日期')
    update_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='更新人名称')
    update_by = models.CharField(max_length=50, blank=True, null=True, verbose_name='更新人登录名称')
    update_date = models.DateTimeField(blank=True, null=True, verbose_name='更新日期')
    sys_org_code = models.CharField(max_length=50, blank=True, null=True, verbose_name='所属部门')
    sys_company_code = models.CharField(max_length=50, blank=True, null=True, verbose_name='所属公司')
    bpm_status = models.CharField(max_length=32, blank=True, null=True, verbose_name='流程状态')
    channel_name = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name='渠道名称')
    channel_describe = models.TextField(max_length=1000, blank=True, null=True, verbose_name='渠道描述')
    organization_id = models.CharField(max_length=36, blank=True, null=True, verbose_name='所属公司')
    channel_key = models.CharField(max_length=255, blank=True, null=True, verbose_name='渠道关键字')
    channel_color = models.CharField(max_length=32, blank=True, null=True, verbose_name='渠道颜色')
    channel_tag = models.CharField(max_length=45, blank=True, null=True, verbose_name='渠道图标标志')

    class Meta:
        managed = False
        app_label = 'Channel'
        db_table = 'yisheng_channel'




class Contract(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid1().hex, max_length=36, editable=False, verbose_name='ID')
    create_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='创建人名称')
    create_by = models.CharField(max_length=50, blank=True, null=True, verbose_name='创建人登录名称')
    create_date = models.DateTimeField(blank=True, null=True, verbose_name='创建日期')
    update_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='更新人名称')
    update_by = models.CharField(max_length=50, blank=True, null=True, verbose_name='更新人登录名称')
    update_date = models.DateTimeField(blank=True, null=True, verbose_name='更新日期')
    sys_org_code = models.CharField(max_length=50, blank=True, null=True, verbose_name='所属部门')
    sys_company_code = models.CharField(max_length=50, blank=True, null=True, verbose_name='所属公司')
    bpm_status = models.CharField(max_length=32, blank=True, null=True, verbose_name='流程状态')
    user_id_back = models.CharField(max_length=36, blank=True, null=True, verbose_name='用户')
    username = models.CharField(max_length=50, blank=True, null=True, verbose_name='用户名')
    channel_id = models.CharField(max_length=32, blank=True, null=True, verbose_name='推广平台')
    sign_date = models.DateTimeField(max_length=32, blank=True, null=True, verbose_name='签约时间')
    expire_date = models.DateTimeField(max_length=32, blank=True, null=True, verbose_name='合同到期时间')
    service_cycle = models.CharField(max_length=32, blank=True, null=True, verbose_name='服务周期')
    service_price = models.CharField(max_length=32, blank=True, null=True, verbose_name='服务费用')
    ad_online_date = models.DateTimeField(max_length=32, blank=True, null=True, verbose_name='广告上线时间')
    ad_offline_date = models.DateTimeField(max_length=32, blank=True, null=True, verbose_name='广告到期时间')
    if_effective = models.CharField(max_length=2, blank=True, null=True, verbose_name='是否有效')
    remark = models.TextField(blank=True, null=True, verbose_name='备注')
    employee_name = models.CharField(max_length=32, blank=True, null=True, verbose_name='员工名称')
    employee_num = models.CharField(max_length=255, blank=True, null=True, verbose_name='员工号码')
    crp_id = models.IntegerField(blank=True, null=True, verbose_name='续费负责人ID')

    class Meta:
        managed = False
        app_label = 'Contract'
        db_table = 'yisheng_contract'



class FtpUser(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid1().hex, max_length=36, editable=False, verbose_name='ID')
    create_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='创建人名称')
    create_by = models.CharField(max_length=50, blank=True, null=True, verbose_name='创建人登录名称')
    create_date = models.DateTimeField(blank=True, null=True, verbose_name='创建日期')
    update_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='更新人名称')
    update_by = models.CharField(max_length=50, blank=True, null=True, verbose_name='更新人登录名称')
    update_date = models.DateTimeField(blank=True, null=True, verbose_name='更新日期')
    sys_org_code = models.CharField(max_length=50, blank=True, null=True, verbose_name='所属部门')
    sys_company_code = models.CharField(max_length=50, blank=True, null=True, verbose_name='所属公司')
    bpm_status = models.CharField(max_length=32, blank=True, null=True, verbose_name='流程状态')

    ftp_url = models.CharField(max_length=32, blank=True, null=True, verbose_name='ftp链接')
    ftp_username = models.CharField(max_length=32, blank=True, null=True, verbose_name='ftp用户名')
    ftp_password = models.CharField(max_length=32, blank=True, null=True, verbose_name='ftp密码')
    site_id = models.CharField(max_length=32, blank=True, null=True, verbose_name='所属网站')
    ftp_index_url = models.CharField(max_length=100, blank=True, null=True, verbose_name='所属网站存放路径')
    ftp_html_file = models.CharField(max_length=32, blank=True, null=True, verbose_name='html文件名')
    ftp_bridge_url = models.CharField(max_length=100, blank=True, null=True, verbose_name='商桥路径')
    ftp_bridge_html_file = models.CharField(max_length=32, blank=True, null=True, verbose_name='商桥html文件')
    site_server = models.CharField(max_length=2, blank=True, null=True, verbose_name='网站服务器')
    custom_port = models.CharField(max_length=8, blank=True, null=True, verbose_name='自定义端口')
    is_installed = models.CharField(max_length=4, blank=True, null=True, verbose_name='是否已安装')
    is_installed_bridge = models.CharField(max_length=4, blank=True, null=True, verbose_name='是否安装代码')
    site_en_name = models.CharField(unique=True, max_length=100, blank=True, null=True, verbose_name='网站英文名')
    user_name = models.CharField(max_length=32, blank=True, null=True, verbose_name='用户名')
    audit = models.CharField(max_length=4, blank=True, null=True, verbose_name='审核状态')
    site_company = models.CharField(max_length=32, blank=True, null=True, verbose_name='维护公司名称')
    sc_phone = models.CharField(max_length=32, blank=True, null=True, verbose_name='联系电话')
    sc_qq = models.CharField(max_length=32, blank=True, null=True, verbose_name='联系qq')
    remark = models.TextField(blank=True, null=True, verbose_name='备注')

    class Meta:
        managed = False
        app_label = 'FtpUser'
        db_table = 'yisheng_ftp_user'


class Industry(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid1().hex, max_length=36, editable=False, verbose_name='ID')
    create_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='创建人名称')
    create_by = models.CharField(max_length=50, blank=True, null=True, verbose_name='创建人登录名称')
    create_date = models.DateTimeField(blank=True, null=True, verbose_name='创建日期')
    update_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='更新人名称')
    update_by = models.CharField(max_length=50, blank=True, null=True, verbose_name='更新人登录名称')
    update_date = models.DateTimeField(blank=True, null=True, verbose_name='更新日期')
    sys_org_code = models.CharField(max_length=50, blank=True, null=True, verbose_name='所属部门')
    sys_company_code = models.CharField(max_length=50, blank=True, null=True, verbose_name='所属公司')
    bpm_status = models.CharField(max_length=32, blank=True, null=True, verbose_name='流程状态')
    industry = models.CharField(max_length=32, unique=True, blank=True, null=True, verbose_name='所属行业名称')
    # second_industry = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        app_label = 'Industry'
        db_table = 'yisheng_industry'



class Optimization(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True, verbose_name='ID')
    create_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='创建人名称')
    create_by = models.CharField(max_length=50, blank=True, null=True, verbose_name='创建人登录名称')
    create_date = models.DateTimeField(blank=True, null=True, verbose_name='创建日期')
    update_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='更新人名称')
    update_by = models.CharField(max_length=50, blank=True, null=True, verbose_name='更新人登录名称')
    update_date = models.DateTimeField(blank=True, null=True, verbose_name='更新日期')
    sys_org_code = models.CharField(max_length=50, blank=True, null=True, verbose_name='所属部门')
    sys_company_code = models.CharField(max_length=50, blank=True, null=True, verbose_name='所属公司')
    bpm_status = models.CharField(max_length=32, blank=True, null=True, verbose_name='流程状态')
    industry_id = models.CharField(max_length=36, blank=True, null=True, verbose_name='所属行业')
    consult_count_max = models.IntegerField(blank=True, null=True, verbose_name='总咨询次数_大于等于')
    consult_count_min = models.IntegerField(blank=True, null=True, verbose_name='总咨询次数_小于')
    consult_cost_max = models.FloatField(blank=True, null=True, verbose_name='总转化成本 _大于等于')
    consult_cost_min = models.FloatField(blank=True, null=True, verbose_name='总转化成本 _小于')
    advice = models.TextField(max_length=2000, blank=True, null=True, verbose_name='建议')
    item_id = models.CharField(max_length=36, blank=True, null=True, verbose_name='套餐商品')
    name = models.CharField(max_length=32, blank=True, null=True, verbose_name='优化建议_名称')

    class Meta:
        managed = False
        app_label = 'Optimization'
        db_table = 'yisheng_optimization'


class YishengUser(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False, verbose_name='ID')
    id = models.CharField(primary_key=True, default=uuid.uuid1().hex, max_length=36, editable=False, verbose_name='ID')
    create_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='创建人名称')
    create_by = models.CharField(max_length=50, blank=True, null=True, verbose_name='创建人登录名称')
    create_date = models.DateTimeField(blank=True, null=True, verbose_name='创建日期')
    update_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='更新人名称')
    update_by = models.CharField(max_length=50, blank=True, null=True, verbose_name='更新人登录名称')
    update_date = models.DateTimeField(blank=True, null=True, verbose_name='更新日期')
    sys_org_code = models.CharField(max_length=50, blank=True, null=True, verbose_name='所属部门')
    sys_company_code = models.CharField(max_length=50, blank=True, null=True, verbose_name='所属公司')
    bpm_status = models.CharField(max_length=32, blank=True, null=True, verbose_name='流程状态')
    username = models.CharField(unique=True, max_length=255, verbose_name='用户名')
    password = models.CharField(max_length=64, verbose_name='密码')
    email = models.CharField(max_length=255, blank=True, null=True, verbose_name='邮箱')
    mobile = models.CharField(max_length=11, blank=True, null=True, verbose_name='手机')
    tel_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='电话')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='地址')
    postcode = models.CharField(max_length=12, blank=True, null=True, verbose_name='邮编')
    idnumber = models.CharField(max_length=20, blank=True, null=True, verbose_name='身份证号码')
    role_id = models.CharField(max_length=36, blank=True, null=True, verbose_name='角色')
    user_status = models.IntegerField(blank=True, null=True, verbose_name='用户状态')
    customer_name = models.CharField(max_length=32, blank=True, null=True, verbose_name='客户姓名')
    company_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='客户公司名称')
    first_online_date = models.CharField(max_length=32, blank=True, null=True, verbose_name='首次上线日期')
    pay_status = models.CharField(max_length=32, blank=True, null=True, verbose_name='付费状态')
    sales_department = models.CharField(max_length=32, blank=True, null=True, verbose_name='销售部门')
    sales_name = models.CharField(max_length=32, blank=True, null=True, verbose_name='销售姓名')
    if_give_wap = models.CharField(max_length=32, blank=True, null=True, verbose_name='是否赠送wap站')
    remark = models.TextField(blank=True, null=True, verbose_name='备注')
    is_synchronized_industry = models.CharField(max_length=2, blank=True, null=True, verbose_name='是否关联到新行业')
    # 用于KAD系统关联
    company_id = models.IntegerField(blank=True, null=True, verbose_name='公司id')
    # Field name made lowercase.
    user_id_kad = models.IntegerField(db_column='user_id_KAD', blank=True, null=True, verbose_name='所属sem用户id')
    company_state = models.CharField(max_length=2, blank=True, null=True, verbose_name='代运营公司状态')
    sys_user_id = models.CharField(max_length=50, blank=True, null=True, verbose_name='系统用户id-saler')
    phone_pay = models.CharField(max_length=32, blank=True, null=True, verbose_name='签约用户联系手机号')
    account_state = models.CharField(max_length=2, blank=True, null=True, verbose_name='账户推广状态')
    app_source = models.CharField(max_length=255, blank=True, null=True, verbose_name='数据源')

    class Meta:
        app_label = 'YishengUser'
        managed = False
        db_table = 'yisheng_user'


class HelpInstruction(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True, verbose_name='ID')
    create_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='创建人名称')
    create_by = models.CharField(max_length=50, blank=True, null=True, verbose_name='创建人登录名称')
    create_date = models.DateTimeField(blank=True, null=True, verbose_name='创建日期')
    update_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='更新人名称')
    update_by = models.CharField(max_length=50, blank=True, null=True, verbose_name='更新人登录名称')
    update_date = models.DateTimeField(blank=True, null=True, verbose_name='更新日期')
    sys_org_code = models.CharField(max_length=50, blank=True, null=True, verbose_name='所属部门')
    sys_company_code = models.CharField(max_length=50, blank=True, null=True, verbose_name='所属公司')
    bpm_status = models.CharField(max_length=32, blank=True, null=True, verbose_name='流程状态')
    keyword = models.TextField(blank=True, null=True, verbose_name='关键词解释')
    question = models.TextField(blank=True, null=True, verbose_name='常见问题')
    userprotocol = models.TextField(blank=True, null=True, verbose_name='用户协议')

    class Meta:
        managed = False
        app_label = 'HelpInstruction'
        db_table = 'yisheng_help_instruction'



class HitAvgPrice(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True, verbose_name='ID')
    create_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='创建人名称')
    create_by = models.CharField(max_length=50, blank=True, null=True, verbose_name='创建人登录名称')
    create_date = models.DateTimeField(blank=True, null=True, verbose_name='创建日期')
    update_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='更新人名称')
    update_by = models.CharField(max_length=50, blank=True, null=True, verbose_name='更新人登录名称')
    update_date = models.DateTimeField(blank=True, null=True, verbose_name='更新日期')
    sys_org_code = models.CharField(max_length=50, blank=True, null=True, verbose_name='所属部门')
    sys_company_code = models.CharField(max_length=50, blank=True, null=True, verbose_name='所属公司')
    bpm_status = models.CharField(max_length=32, blank=True, null=True, verbose_name='流程状态')
    site_name = models.CharField(max_length=32, blank=True, null=True, verbose_name='网站名')
    channe_name = models.CharField(max_length=32, blank=True, null=True, verbose_name='推广渠道')
    site_channel = models.CharField(max_length=32, blank=True, null=True, verbose_name='网站名')
    site_id = models.CharField(max_length=32, blank=True, null=True, verbose_name='用户网站id')
    hit_avg_price = models.FloatField(blank=True, null=True, verbose_name='平均点击价格')
    user_name = models.CharField(max_length=32, blank=True, null=True, verbose_name='用户名')
    user_id = models.CharField(max_length=32, blank=True, null=True, verbose_name='用户id')
    bind_phone = models.CharField(max_length=32, blank=True, null=True, verbose_name='绑定手机')
    login_password = models.CharField(max_length=32, blank=True, null=True, verbose_name='推广账号密码')
    budget_day = models.CharField(max_length=32, blank=True, null=True, verbose_name='日预算')
    login_name = models.CharField(max_length=32, blank=True, null=True, verbose_name='推广账号名称')
    company_id = models.IntegerField(blank=True, null=True, verbose_name='公司id')
    type_tag = models.CharField(max_length=50, blank=True, null=True, verbose_name='推广平台类型')
    ad_online_date = models.DateTimeField(blank=True, null=True, verbose_name='广告上线时间')
    ad_offline_date = models.DateTimeField(blank=True, null=True, verbose_name='广告到期时间')

    class Meta:
        managed = False
        app_label = 'HitAvgPrice'
        db_table = 'yisheng_hit_avg_price'


class UserSites(models.Model):
    id = models.CharField(primary_key=True, default=uuid.uuid1().hex, max_length=36, editable=False, verbose_name='ID')
    create_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='创建人名称')
    create_by = models.CharField(max_length=50, blank=True, null=True, verbose_name='创建人登录名称')
    create_date = models.DateTimeField(blank=True, null=True, verbose_name='创建日期')
    update_name = models.CharField(max_length=50, blank=True, null=True, verbose_name='更新人名称')
    update_by = models.CharField(max_length=50, blank=True, null=True, verbose_name='更新人登录名称')
    update_date = models.DateTimeField(blank=True, null=True, verbose_name='更新日期')
    bpm_status = models.CharField(max_length=32, blank=True, null=True, verbose_name='流程状态')
    site_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='网站名称')
    domain = models.CharField(unique=True, max_length=255, verbose_name='域名')
    user_id = models.CharField(max_length=32, blank=True, null=True, verbose_name='用户')
    hit_avg_price = models.CharField(max_length=8, blank=True, null=True, verbose_name='平均点击价格')
    industry_id = models.CharField(max_length=32, blank=True, null=True, verbose_name='所属行业')
    has_data = models.CharField(max_length=4, blank=True, null=True, verbose_name='是否连接成功')
    last_detection_time = models.DateTimeField(blank=True, null=True, verbose_name='上次检测时间')
    display_domain = models.CharField(max_length=255, blank=True, null=True, verbose_name='展示域名')

    class Meta:
        managed = False
        app_label = 'UserSites'
        db_table = 'yisheng_user_sites'
