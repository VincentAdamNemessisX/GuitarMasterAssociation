# Generated by Django 3.2.15 on 2023-12-20 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_alter_recentbrowsing_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_phone',
            field=models.CharField(db_index=True, max_length=22),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_qq',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
    ]
