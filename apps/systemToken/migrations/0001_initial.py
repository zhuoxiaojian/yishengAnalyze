# Generated by Django 2.0 on 2018-10-19 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SystemToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=255, verbose_name='token')),
            ],
            options={
                'verbose_name': '系统用户令牌',
                'verbose_name_plural': '系统用户令牌',
                'db_table': 'system_token',
            },
        ),
    ]
