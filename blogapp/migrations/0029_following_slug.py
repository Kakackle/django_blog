# Generated by Django 4.2.1 on 2023-08-10 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0028_following_unique_following_relation'),
    ]

    operations = [
        migrations.AddField(
            model_name='following',
            name='slug',
            field=models.SlugField(default='temp'),
        ),
    ]
