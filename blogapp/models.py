from django.db import models
from django.contrib.auth.models import User
# from froala_editor.fields import FroalaField
from tinymce import models as tinymce_models

STATUS_CHOICES = (
   ('draft', 'Draft'),
   ('published', 'Published'),
)

class Category(models.Model):
    category = models.CharField(max_length = 250, unique=True)
    img = models.ImageField(null = True)
    desc = models.TextField(blank=True)

    def __str__(self):
        return self.category

class Carousel(models.Model):
    title = models.CharField(max_length = 250)
    img = models.ImageField()
    exp = models.DateTimeField()

    def __str__(self):
        return self.title

class Post(models.Model):
    author = models.ForeignKey(User, null = True, on_delete = models.SET_NULL)
    category = models.ForeignKey(Category, null = True, on_delete = models.SET_NULL)
    title = models.CharField(max_length = 250)
    desc = models.CharField(max_length = 500, blank=True)
    slug = models.SlugField(max_length = 300, null = True, blank = True)
    # body = FroalaField()
    body = tinymce_models.HTMLField()
    published_at = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    status = models.CharField(max_length = 10, choices = STATUS_CHOICES, default ='draft')
    
    
    class Meta:
        ordering = ('-published_at', )
    
    def __str__(self):
        return self.title

class Image(models.Model):
    name = models.CharField(max_length = 100)
    # desc = models.CharField(max_length = 300, null = True)
    category = models.ForeignKey(Category, null = True, on_delete = models.SET_NULL)
    url = models.URLField(max_length = 500)

    def __str__(self):
        return self.name