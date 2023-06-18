# Generated by Django 4.2.1 on 2023-06-18 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0014_post_likes_alter_post_date_posted'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='liked_posts',
            field=models.ManyToManyField(related_name='liked_by', to='blogapp.post'),
        ),
    ]
