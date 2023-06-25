from django.contrib import admin
from .models import User, Tag, Post, Comment, ImagePost

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(ImagePost)
