# Generated by Django 4.2.1 on 2023-06-18 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0015_user_liked_posts'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
    ]
