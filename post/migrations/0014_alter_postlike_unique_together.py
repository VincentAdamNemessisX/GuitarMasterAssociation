# Generated by Django 3.2.15 on 2023-12-22 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_rename_recent_create_time_recentbrowsing_recent_browsing_time'),
        ('post', '0013_postlike'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='postlike',
            unique_together={('user_id', 'post_id')},
        ),
    ]