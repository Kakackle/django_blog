# Generated by Django 4.2.1 on 2023-06-24 10:08

import blogapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0022_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to=blogapp.models.upload_to_cover),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=blogapp.models.upload_to_avatar),
        ),
        migrations.AlterField(
            model_name='user',
            name='liked_comments',
            field=models.ManyToManyField(blank=True, related_name='liked_by', to='blogapp.comment'),
        ),
        migrations.AlterField(
            model_name='user',
            name='liked_posts',
            field=models.ManyToManyField(blank=True, related_name='liked_by', to='blogapp.post'),
        ),
    ]
