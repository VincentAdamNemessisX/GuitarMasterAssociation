# Generated by Django 3.2.15 on 2023-12-07 12:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0004_remove_review_review_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review_time_index',
            field=models.DateTimeField(db_index=True, default=django.utils.timezone.now),
        ),
    ]