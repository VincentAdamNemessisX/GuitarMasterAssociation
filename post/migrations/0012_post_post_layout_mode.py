# Generated by Django 3.2.15 on 2023-12-14 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0011_remove_post_post_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_layout_mode',
            field=models.CharField(choices=[('normal', '普通'), ('immersion', '沉浸式')], default='normal', max_length=20),
        ),
    ]
