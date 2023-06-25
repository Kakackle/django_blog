# Generated by Django 4.2.1 on 2023-06-25 15:41

import blogapp.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0023_alter_post_img_alter_user_avatar_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to=blogapp.models.ImagePost.image_dir)),
                ('slug', models.SlugField(default='temp', unique=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_images', to='blogapp.post')),
            ],
        ),
    ]
