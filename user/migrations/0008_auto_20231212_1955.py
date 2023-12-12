# Generated by Django 3.2.15 on 2023-12-12 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20231212_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_last_active_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_description',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_nickname',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
    ]