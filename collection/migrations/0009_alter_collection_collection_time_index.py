# Generated by Django 3.2.15 on 2023-12-16 09:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0008_alter_collection_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='collection_time_index',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 12, 16, 9, 41, 5, 652691, tzinfo=utc)),
        ),
    ]
