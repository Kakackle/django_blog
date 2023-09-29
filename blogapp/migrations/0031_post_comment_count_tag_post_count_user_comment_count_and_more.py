# Generated by Django 4.2.1 on 2023-08-11 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0030_alter_following_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='comment_count',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='tag',
            name='post_count',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='comment_count',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='comment_likes_received',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='followed_by_count',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='followed_count',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='post_count',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='post_likes_received',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]