from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect

from django.contrib.auth.forms import UserCreationForm

# Create your views here.
from django.contrib.auth.decorators import login_required
# from .decorators import allowed_users,admin_only
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def logoutuser(request):
	logout(request)
	return redirect('home')






def login_page(request):
	if request.method =='POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request,username=username,password=password)
		if user is not None:
			login(request,user)
			return redirect('home')
		else:
			messages.info(request,'User or Password is Incorrect')

	context={}
	return render(request,'pages/login.html',context)



def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        

    context = {'form':form}
    return render(request, 'pages/register.html', context)


def business_registerPage(request):
    form = busines_resgiter_form(initial = {'status':'pending'})
    if request.method == 'POST':
        form = busines_resgiter_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_page')
        

    context = {'form':form}
    return render(request, 'pages/business_register.html', context)



def home(request):
    all_salons = Salon.objects.all()
    context={'all_salons':all_salons}
    return render(request,'pages/home.html',context)



def register_option(request):
    context={}
    return render(request,'pages/register_option.html',context)




def admin_home(request):
    all_requests = BusinessRegister.objects.all()
    context={'all_requests':all_requests}
    return render(request,'pages/admin_panel.html',context)


# def blog_view(request,id):
#     blog = Salons.objects.get(id=id)
#     check = False
#     if blog.language == 'English':
#         check = True

#     context={'blog':blog,'check':check}
#     return render(request,'pages/article.html',context)



# @login_required(login_url=login_page)
# @allowed_users(allowed_roles=['admin'])
# def user_home(request):
#     all_blogs = Blog.objects.all()
#     context={'all_blogs':all_blogs}
#     return render(request,'pages/user_panel.html',context)


def new_blog(request):
    form = new_salon_form(request.POST,request.FILES)
    files = request.FILES.getlist('thumbnail')
    files1 = request.FILES.getlist('title_image')
    files2 = request.FILES.getlist('center_image')
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            for image in files:
                obj.thumbnail = image
                obj.save()
            for imag in files1:
                obj.title_image = imag
                obj.save()
            for img in files2:
                obj.center_image = img
                obj.save()        
            return redirect('user_home')
	
    context = {'form':form}
    return render(request,'pages/new_salon.html',context)


# @login_required(login_url=login_page)
# @allowed_users(allowed_roles=['admin'])
# def edit_blog(request,id):
#     blog_to_edit = Blog.objects.get(id=id)
#     form = new_blog_form(instance=blog_to_edit)
#     files = request.FILES.getlist('thumbnail')
#     if request.method == 'POST':
#         form = new_blog_form(request.POST,instance=blog_to_edit)
#         if form.is_valid():
#             obj = form.save()
#             for image in files:
#                 obj.thumbnail = image
#                 obj.save()
#             return redirect('user_home')
	
#     context = {'form':form}
#     return render(request,'pages/edit_blog.html',context)