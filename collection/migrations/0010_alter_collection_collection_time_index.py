# Generated by Django 3.2.15 on 2023-12-16 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0009_alter_collection_collection_time_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='collection_time_index',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
    ]