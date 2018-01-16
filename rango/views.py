from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm

def index(request):

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    #link to template and provide dictionary for Django variables within templates
    context_dict = {'categories': category_list,
                    'pages': page_list}

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

def add_category(request):
    form = CategoryForm()
    
    if request.method == "POST":
        form = CategoryForm(request.POST)

    #Is the form valid?
    if form.is_valid():
        #save category to db
        form.save(commit=True)
        #go back to index page
        return index(request)
    else:
        #if form is erroneous, tell the user what was wrong
        print(form.errors)

    return render(request, 'rango/add_category.html', {'form' : form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
            else:
                print(form.errors)

    context_dict = {'form':form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)

def register(request):
    # Shows whether registration was successful
    registered = False

    # If it's HTTP POST, we want the info from the form
    if request.method == 'POST':
        # Try to gather information
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the forms are valid, save the user's form data
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            # If a picture is provided, we want to include that in the profile
            if 'picture' in request.FILES:
                profile.picture = request.FILES('picture')

            # Save profile to db
            profile.save()

            # Show registration was successful
            registered = True
        else:
            # Print problems to terminal
            print(user_form.errors, profile_form.errors)
    else:
        # Not HTTP POST, so we present forms for user input
        user_form = UserForm()
        profile_form = UserProfileForm()

    #Render template based on context
    return render(request,
                  'rango/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})
            
