# Generated by Django 3.2.15 on 2023-12-12 04:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('post', '0006_auto_20231208_1441'),
        ('user', '0004_auto_20231211_2007'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecentBrowsing',
            fields=[
                ('recent_id', models.AutoField(primary_key=True, serialize=False)),
                ('recent_post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.post')),
                ('recent_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'verbose_name': '最近浏览',
                'verbose_name_plural': '最近浏览',
                'db_table': 'recent_browsing',
            },
        ),
    ]
