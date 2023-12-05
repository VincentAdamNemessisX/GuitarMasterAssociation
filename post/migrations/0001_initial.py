# Generated by Django 3.2.15 on 2023-12-05 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('zone_id', models.IntegerField()),
                ('post_title', models.CharField(max_length=200)),
                ('post_content', models.TextField()),
                ('post_time', models.DateTimeField(auto_now_add=True)),
                ('post_status', models.IntegerField()),
                ('post_view', models.IntegerField(default=0)),
                ('post_like', models.IntegerField(default=0)),
                ('post_comment', models.IntegerField(default=0)),
                ('post_favorite', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': '帖子管理',
                'verbose_name_plural': '帖子管理',
            },
        ),
    ]
