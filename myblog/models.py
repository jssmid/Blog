from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField

# -----------------------------------------------------------------------------

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# -----------------------------------------------------------------------------

class Post(models.Model):
    author =  models.ForeignKey(User, on_delete=models.SET_NULL , null=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True,upload_to='media/images/')
    slug = models.SlugField(max_length=100, blank=True, null=True)
    content = RichTextUploadingField(blank=True, null=True)
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True )
    created = models.DateField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug is None:
             self.slug = slugify(self.title)
        
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created']

# ----------------------------------------------------------------------------