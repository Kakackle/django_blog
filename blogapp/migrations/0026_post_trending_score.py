# Generated by Django 4.2.1 on 2023-08-08 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0025_alter_comment_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='trending_score',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
