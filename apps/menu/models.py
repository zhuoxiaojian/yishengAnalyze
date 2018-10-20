from django.db import models

# Create your models here.
class Menu(models.Model):
    is_parent = models.BooleanField(verbose_name='是否根菜单', null=False, blank=False, default=False)
    name = models.CharField(max_length=255, verbose_name='菜单名称', null=False, blank=False)
    path = models.CharField(max_length=255, verbose_name='路径', null=False, blank=False)
    parentId = models.IntegerField(verbose_name='父菜单', default=None, null=True, blank=True)
    iconCls = models.CharField(max_length=255, verbose_name='菜单图标', null=True, blank=True)
    menuCode = models.CharField(max_length=255, verbose_name='菜单编码', null=False, blank=False, unique=True)
    menuShow = models.BooleanField(verbose_name='是否展示', null=False, blank=False, default=True)
    leaf = models.BooleanField(verbose_name='是否一个节点', null=False, blank=False, default=False)
    class Meta:
        db_table = 'ys_menu'
        verbose_name = '菜单管理'
        verbose_name_plural = verbose_name



    def __str__(self):
        return self.name


    def showParent(self):
        if self.parentId:
            menu = Menu.objects.get(id=self.parentId)
            return menu.name
        return None

    showParent.short_description = '父菜单'

