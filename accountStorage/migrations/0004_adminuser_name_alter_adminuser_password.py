# Generated by Django 4.1.1 on 2022-11-18 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accountStorage', '0003_adminuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminuser',
            name='name',
            field=models.CharField(max_length=32, null=True, verbose_name='名称'),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='password',
            field=models.CharField(max_length=128, verbose_name='密码'),
        ),
    ]