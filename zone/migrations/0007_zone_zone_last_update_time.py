# Generated by Django 3.2.15 on 2023-12-15 07:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('zone', '0006_zone_zone_create_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='zone',
            name='zone_last_update_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
