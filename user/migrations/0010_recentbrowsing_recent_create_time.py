# Generated by Django 3.2.15 on 2023-12-13 05:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20231212_2010'),
    ]

    operations = [
        migrations.AddField(
            model_name='recentbrowsing',
            name='recent_create_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
