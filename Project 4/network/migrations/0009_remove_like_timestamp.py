# Generated by Django 5.0 on 2023-12-30 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_like_timestamp_alter_like_post_alter_like_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='timestamp',
        ),
    ]
