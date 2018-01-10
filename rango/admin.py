from django.contrib import admin
#Import database models
from rango.models import Category, Page
# Register your models here.

admin.site.register(Category)

# Introduce class for customisation
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

admin.site.register(Page, PageAdmin)
