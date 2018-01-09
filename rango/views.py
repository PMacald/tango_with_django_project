from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    #link to template and provide dictionary for Django variables within templates
    context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    #Get rendered response for client
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    #link to template and provide dictionary for Django variables within templates
    context_dict = {'aboutmessage': "This tutorial has been put together by Peter Macaldowie."}
    #Get rendered response for client
    return render(request, 'rango/about.html', context=context_dict)
