# Generated by Django 3.2.15 on 2023-12-14 07:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0009_post_post_image'),
        ('user', '0013_alter_recentbrowsing_recent_post_id'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='recentbrowsing',
            unique_together={('recent_post_id', 'recent_user_id')},
        ),
    ]
