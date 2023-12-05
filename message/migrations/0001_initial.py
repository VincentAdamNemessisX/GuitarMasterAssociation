# Generated by Django 3.2.15 on 2023-12-05 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('message_id', models.AutoField(primary_key=True, serialize=False)),
                ('sender_id', models.IntegerField(db_index=True)),
                ('receiver_id', models.IntegerField(db_index=True)),
                ('message_content', models.TextField()),
                ('message_time', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('message_status', models.IntegerField(db_index=True)),
                ('message_type', models.IntegerField()),
            ],
            options={
                'verbose_name': '消息管理',
                'verbose_name_plural': '消息管理',
            },
        ),
    ]
