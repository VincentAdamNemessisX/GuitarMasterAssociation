# Generated by Django 3.2.15 on 2023-12-15 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zone', '0003_alter_zone_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='zone',
            name='zone_layout_mode',
            field=models.IntegerField(choices=[(1, '普通'), (2, '沉浸式')], default=1),
        ),
    ]