# Generated by Django 4.2.1 on 2023-08-10 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0027_following'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='following',
            constraint=models.UniqueConstraint(fields=('user', 'following_user'), name='unique_following_relation'),
        ),
    ]