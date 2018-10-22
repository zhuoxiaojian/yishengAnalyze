from django.db import models

# Create your models here.
class YiShengUser(models.Model):
    username = models.CharField(max_length=255, verbose_name='账号', null=False, blank=False, unique=True)
    password = models.CharField(max_length=255, verbose_name='密码', null=False, blank=False)
    company_name = models.CharField(max_length=255, verbose_name='公司名', null=True, blank=True)

    class Meta:
        app_label = 'yiShengUser'
        db_table = 'yisheng_user'
        verbose_name = '易数宝用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
