# Generated by Django 4.2.1 on 2023-06-23 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0019_alter_comment_options_rename_user_comment_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='slug',
            field=models.SlugField(default='empty', unique=True),
        ),
    ]
