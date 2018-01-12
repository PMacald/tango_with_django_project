from django.db import models
from django.template.defaultfilters import slugify
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
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
