# Generated by Django 3.2.15 on 2023-12-07 12:52

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('collection', '0004_alter_collection_collection_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='collection_time_index',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
    ]
