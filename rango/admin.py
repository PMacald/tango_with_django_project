from django.contrib import admin
#Import database models
from rango.models import Category, Page
from rango.models import UserProfile



# Introduce class for customisation
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category,CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
