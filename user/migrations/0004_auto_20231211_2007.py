# Generated by Django 3.2.15 on 2023-12-11 12:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('user', '0003_auto_20231211_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_email',
            field=models.CharField(db_index=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_phone',
            field=models.CharField(db_index=True, max_length=11),
        ),
    ]
