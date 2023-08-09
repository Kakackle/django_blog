from django.db import models
from django.template.defaultfilters import slugify
from django.utils import timezone
from django.utils.crypto import get_random_string
import datetime
class Tag(models.Model):
    """
    Tag object for posts, shared between posts
    """
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=500)
    slug = models.SlugField(null=False, unique=True, default='temp')
    # slug = models.SlugField(default='tag', null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # if not self.slug:
        if self.slug == 'temp':
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

# Pozwoli sprecyzowac folder to ktorego beda uploadowane obrazki zamiast
# Ogolnego sprecyzowanego w settings
def upload_to_avatar(instance, filename):
    random_str = get_random_string(length=8)
    return 'images/avatars/{filename}-{random}'.format(
        filename=filename, random=random_str)

def upload_to_cover(instance, filename):
    random_str = get_random_string(length=8)
    return 'images/covers/{filename}'.format(
        filename=filename, random=random_str)

class User(models.Model):
    """
    Blog user model (most likely to be turned into a profile
    with a separate user model with a one to one relation)
    """
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    mail = models.EmailField(max_length=100)
    bio = models.CharField(max_length=500)
    # avatar = models.URLField(max_length=250)
    avatar = models.ImageField(null=True, blank=True, upload_to=upload_to_avatar)
    # slug = models.SlugField(default='slug', null=True)
    slug = models.SlugField(null=False, unique=True, default='temp')
    liked_posts = models.ManyToManyField('Post', related_name="liked_by", blank=True)
    liked_comments = models.ManyToManyField('Comment', related_name='liked_by', blank=True)
    
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if self.slug == 'temp':
            self.slug = slugify(self.username)
        return super().save(*args, **kwargs)

class Post(models.Model):
    """
    Blog post
    poki co bez UUID itp,
    pola nie ostateczne, zobaczymy jak beda dzialac obrazki itd
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name="posts")
    date_posted = models.DateField()
    date_updated = models.DateField(auto_now=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name="posts")
    content = models.TextField()
    # img = models.URLField(max_length=250)
    img = models.ImageField(null=True, blank=True, upload_to=upload_to_cover)
    views = models.IntegerField(default=0, blank=True)
    # liked_by = models.JSONField(null=True)
    likes = models.IntegerField(default=0, blank=True)
    slug = models.SlugField(null=False, unique=True, default='temp')
    trending_score = models.FloatField(default=0, blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # if not self.slug:
        if self.slug == 'temp':
            self.slug = slugify(self.title)
        # if self.likes == 0 and self.liked_by:
        #     self.likes = self.liked_by.all().count()
        delta = timezone.now().date() - self.date_posted
        delta_days = delta.days if delta.days > 0 else 1
        self.trending_score = self.views / delta_days; 
        return super().save(*args, **kwargs)
    
class ImagePost(models.Model):

    def image_dir(self, filename):
        random_str = get_random_string(length=8)
        return 'images/{post}/{filename}-{random}'.format(
            filename=self.name, post=self.post.slug, random=random_str)

    name = models.CharField(max_length=255)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="post_images")
    image = models.ImageField(upload_to=image_dir)
    slug = models.SlugField(null=False, unique=True, default='temp')

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.slug == 'temp':
            self.slug = str(self.post.slug) + '-' + str(self.name)
        return super().save(*args, **kwargs)

class Comment(models.Model):
    """
    Comment object for posts, multiple on one post, one user author
    replies allowed, both as parent and children
    """
    content = models.TextField(max_length=500)
    author = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="comments")
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name="comments")
    date_posted = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    slug = models.SlugField(null=False, unique=True, default="empty")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    likes = models.IntegerField(default=0, blank=True)

    class Meta:
        ordering=['-date_posted']

    def __str__(self):
        # return str(self.author) + str(self.content[:25])
        return str(self.post.slug) + '-' + str(self.author.slug) + '-' + str(self.parent)
    
    @property
    def children(self):
        return Comment.objects.filter(parent=self).reverse()
    
    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
    
    def save(self, *args, **kwargs):
        if self.slug == "empty":
            self.slug = str(self.post.slug) + '-' + str(self.author.slug) + '-' + str(self.parent)
        return super().save(*args, **kwargs)
