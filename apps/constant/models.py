from django.db import models

# Create your models here.
class Constant(models.Model):
    name = models.CharField(max_length=255, verbose_name='键名', null=False, blank=False, unique=True)
    value = models.CharField(max_length=255, verbose_name='键值', null=True, blank=True)
    remark = models.CharField(max_length=255, verbose_name='备注', null=True, blank=True)

    class Meta:
        db_table = 'ys_constant'
        verbose_name = '常量管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
