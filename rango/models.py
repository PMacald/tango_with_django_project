from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

#Models
class Category(models.Model):
    name_max_length = 128
    name = models.CharField(max_length=name_max_length, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name

    #for unicode support of Python 2.x
    def __unicode__(self):
        return self.name

    #Set plural for display
    class Meta:
        verbose_name_plural = 'Categories'

    #Use slugify to determine meaningful urls
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args,**kwargs)

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    #for unicode support of Python 2.x
    def __unicode__(self):
        return self.title

class UserProfile(models.Model):
    #link UserProfile to user
    user = models.OneToOneField(User)

    #Extra attributes to include
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images',blank=True)

    def __str__(self):
        return self.user.username

    #for unicode support of Python 2.x
    def __unicode__(self):
        return self.user.username    
