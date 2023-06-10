from django.db import models
from django.template.defaultfilters import slugify
class Tag(models.Model):
    """
    Tag object for posts, shared between posts
    """
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=500)
    slug = models.SlugField(null=False, unique=True)
    # slug = models.SlugField(default='tag', null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

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
    avatar = models.URLField(max_length=250)
    # slug = models.SlugField(default='slug', null=True)
    slug = models.SlugField(null=False, unique=True)
    
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if not self.slug:
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
    date_posted = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name="posts")
    content = models.CharField(max_length=2000)
    img = models.URLField(max_length=250)
    views = models.IntegerField(default=0, blank=True)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

class Comment(models.Model):
    """
    Comment object for posts, multiple on one post, one user author
    """
    content = models.CharField(max_length=500)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="comments")
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name="comments")
    date_posted = models.DateField(auto_now_add=True)
    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.content[:25]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(self.user.slug) + str(self.post.slug)
        return super().save(*args, **kwargs)
