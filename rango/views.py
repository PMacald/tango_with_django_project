from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.webhose_search import run_query

def index(request):
    
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    #link to template and provide dictionary for Django variables within templates
    context_dict = {'categories': category_list,
                    'pages': page_list}
    # Call helper function to handle cookies
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    
    # Get response early so we can gather cookie info
    response = render(request, 'rango/index.html', context_dict)
    #Get response for client and return it (updating cookies if need be) 
    return response

def about(request):
    #link to template and provide dictionary for Django variables within templates
    context_dict = {'aboutmessage': "rango says here is the about page. This tutorial has been put together by Peter Macaldowie."}

    # Call helper function to handle cookies
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    
    # Get response early so we can gather cookie info
    response = render(request, 'rango/about.html', context_dict)
    #Get response for client and return it (updating cookies if need be) 
    return response

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

"""def register(request):
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
            
def user_login(request):
    if request.method == 'POST':
        # Get username and password from request
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check validity of username and password
        user = authenticate(username=username, password=password)

        # If user exists, the details are correct
        if user:
            if user.is_active:
                login(request,user)
                # Send user to homepage
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('Your Rango account is disabled')
        else:
            print('Invalid login details: {0}, {1}'.format(username,password))
            return HttpResponse("Invalid login details supplied.")
    else:
        # Not a POST method, so we can't use context variables
        return render(request, 'rango/login.html',{})"""
                                
@login_required
def restricted(request):
    return render(request, 'rango/restricted.html',{})


"""@login_required
def user_logout(request):
    logout(request)
    # Redirect to homepage
    return HttpResponseRedirect(reverse('index'))"""

# Helper method
def get_server_side_cookie(request,cookie,default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    # Use cookies to track number of visits. If a previous cookie exists, we can say they've visited before
    # Default value is 1
    visits = int(get_server_side_cookie(request,'visits','1'))

    last_visit_cookie = get_server_side_cookie(request,
                                               'last_visit',
                                               str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')

    # If time since last visit > 1 day, add a visit
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # Update last visit cookie
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        # Set last visit cookie
        request.session['last_visit'] = last_visit_cookie

    # Update visits cookie
    request.session['visits'] = visits

def search(request):
    result_list = []
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            # Run our Webhose search function to get the results list!
            result_list = run_query(query)
            
    return render(request, 'rango/search.html', {'result_list': result_list})
