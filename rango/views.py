from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category
from rango.models import Page

def index(request):

    category_list = Category.objects.order_by('-likes')[:5]
    #link to template and provide dictionary for Django variables within templates
    context_dict = {'categories': category_list}

    #Get rendered response for client and return it
    return render(request, 'rango/index.html', context_dict)

def about(request):
    #link to template and provide dictionary for Django variables within templates
    context_dict = {'aboutmessage': "This tutorial has been put together by Peter Macaldowie."}
    #Get rendered response for client
    return render(request, 'rango/about.html', context=context_dict)

def show_category(request, category_name_slug):
    context_dict = {}
    try:
        #Attempt to find category name slug with given name
        category = Category.objects.get(slug=category_name_slug)

        #Retrieve pages associated with the category
        pages = Page.objects.filter(category=category)

        #Adds results to template context
        context_dict['pages'] = pages

        #Also add categories to context
        context_dict['category'] = category
    except Category.DoesNotExist:
        # Set context to none for error message
        context_dict['category'] = None
        context_dict['pages'] = None

    #Render response and return it
    return render(request, 'rango/category.html', context_dict)
