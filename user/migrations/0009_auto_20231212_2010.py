# Generated by Django 3.2.15 on 2023-12-12 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20231212_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_sex',
            field=models.IntegerField(choices=[(1, '男'), (2, '女'), (3, '保密')], default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_status',
            field=models.IntegerField(choices=[(1, '正常'), (2, '禁用'), (3, '冻结')], default=1),
        ),
    ]
