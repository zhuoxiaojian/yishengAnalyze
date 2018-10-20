# Generated by Django 2.0 on 2018-10-19 21:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('depart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupDepart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('depart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='depart.Depart', verbose_name='部门')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Group', verbose_name='角色')),
            ],
            options={
                'verbose_name': '部门权限',
                'verbose_name_plural': '部门权限',
                'db_table': 'ys_group_depart',
            },
        ),
        migrations.AlterUniqueTogether(
            name='groupdepart',
            unique_together={('group', 'depart')},
        ),
    ]
