from django.db import models

# Create your models here.
class Depart(models.Model):
    is_parent = models.BooleanField(verbose_name='是否根部门', null=False, blank=False, default=False)
    name = models.CharField(max_length=255, verbose_name='部门名称', null=False, blank=False)
    parentId = models.IntegerField(verbose_name='上级部门', default=None, null=True, blank=True)
    departCode = models.CharField(max_length=255, verbose_name='部门编码', null=False, blank=False, unique=True)


    class Meta:
        db_table = 'ys_depart'
        verbose_name = '部门管理'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name