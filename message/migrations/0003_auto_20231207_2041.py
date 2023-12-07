# Generated by Django 3.2.15 on 2023-12-07 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0002_auto_20231207_2004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='message_type',
        ),
        migrations.AlterField(
            model_name='message',
            name='message_status',
            field=models.IntegerField(choices=[(1, '已读'), (0, '未读')], db_index=True, default=1),
        ),
    ]
