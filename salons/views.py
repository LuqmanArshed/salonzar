from .models import *
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

from django.contrib.auth.decorators import login_required
from .decorators import allowed_users,admin_only

from django.db.models import Q






def logoutuser(request):
	logout(request)
	return redirect('login_page')






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
        con = request.POST.get('contact')
        address = request.POST.get('address')
        form = CreateUserForm(request.POST)
        if form.is_valid():
            obj=form.save()
            car = Cart.objects.create(user=obj)
            car.phone = con
            car.address = address
            car.save()
            return redirect('home')
        

    context = {'form':form}
    return render(request, 'pages/register.html', context)


def business_registerPage(request):
    form = busines_resgiter_form(initial={'status':'pending'})
    if request.method == 'POST':
        form = busines_resgiter_form(request.POST,request.FILES)
        files = request.FILES.getlist('thumbnail')
        if form.is_valid():
            obj=form.save()
            for image in files:
                obj.thumbnail = image
                obj.save()
            return redirect('all_sw',obj.id)
        

    context = {'form':form}
    return render(request, 'pages/business_register.html', context)


def workers_services(request,id):
    salon = Salon.objects.get(id=id)
    all_workers = SalonWorker.objects.filter(salon=salon)
    all_services = Service.objects.filter(salon=salon)
    context={'all_workers':all_workers,'s_id':id,'all_services':all_services}
    return render(request,'pages/workers_serivces.html',context)



def worker_registerPage(request,id):
    salon = Salon.objects.get(id=id)
    form = salon_worker_form(initial = {'salon':salon})
    if request.method == 'POST':
        form = salon_worker_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_sw',id)
        

    context = {'form':form}
    return render(request, 'pages/workers_register_page.html', context)



def service_registerPage(request,id):
    salon = Salon.objects.get(id=id)
    form = salon_serice_form(initial = {'salon':salon})
    if request.method == 'POST':
        form = salon_serice_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_sw',id)
        

    context = {'form':form}
    return render(request, 'pages/workers_register_page.html', context)    

@admin_only
def home(request):
    all_salons = Salon.objects.filter(status='approved')
    context={'all_salons':all_salons}
    return render(request,'pages/home.html',context)



@login_required(login_url=login_page)
@allowed_users(allowed_roles=['salon manager'])
def salon_user_page(request):
    user = request.user
    print(user)
    salon = Salon.objects.get(user=user)
    appointments = Order.objects.filter(salon=salon,order_status='inprogress')
    completed = Order.objects.filter(salon=salon,order_status='complete')
    all_workers = SalonWorker.objects.filter(salon=salon)
    all_products = Product.objects.filter(salon=salon)
    context={'salon':salon,'all_workers':all_workers,'appointments':appointments,'completed':completed,'all_products':all_products}
    return render(request,'pages/salon_user.html',context)



@login_required(login_url=login_page)
@allowed_users(allowed_roles=['salon manager'])
def change_order_status(request,id):
    order = Order.objects.get(id=id)
    order.order_status = 'complete'
    order.save()
    return redirect('salon_user')


@login_required(login_url=login_page)
@allowed_users(allowed_roles=['salon manager'])
def add_slot(request,id):
    worker = SalonWorker.objects.get(id=id)
    form = slot_form(initial = {'worker':worker})
    if request.method == 'POST':
        form = slot_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('salon_user')
        

    context = {'form':form}
    return render(request, 'pages/new_slot.html', context)


@login_required(login_url=login_page)
@allowed_users(allowed_roles=['salon manager'])
def add_new_product(request,id):
    salon = Salon.objects.get(id=id)
    form = product_form(initial = {'salon':salon})
    if request.method == 'POST':
        form = product_form(request.POST,request.FILES)
        files = request.FILES.getlist('product_image')
        if form.is_valid():
            obj=form.save()
            for image in files:
                obj.product_image = image
                obj.save()

            return redirect('salon_user')
        

    context = {'form':form}
    return render(request, 'pages/new_product.html', context)

@login_required(login_url=login_page)
@allowed_users(allowed_roles=['salon manager'])
def worker_slots(request,id):
    worker = SalonWorker.objects.get(id=id)
    all_slots = Slot.objects.filter(worker=worker)
    context={'all_slots':all_slots}
    return render(request,'pages/worker_slots.html',context)


def salon_view(request,id):
    salon = Salon.objects.get(id=id)
    salon_services = Service.objects.filter(salon=salon)
    salon_workers = SalonWorker.objects.filter(salon=salon)
    salon_products = Product.objects.filter(salon=salon)
    context={'salon':salon,'salon_services':salon_services, "salon_workers":salon_workers,'salon_products':salon_products}
    return render(request,'pages/salon_view.html',context)





def register_option(request):
    context={}
    return render(request,'pages/register_option.html',context)






@login_required(login_url=login_page)
@allowed_users(allowed_roles=['admin'])
def admin_home(request):
    all_requests = Salon.objects.all()
    context={'all_requests':all_requests}
    return render(request,'pages/admin_panel.html',context)

@login_required(login_url=login_page)
@allowed_users(allowed_roles=['admin'])
def approve_salon(request,id):
    salon = Salon.objects.get(id=id)
    salon.status = 'approved'
    salon.save()
    return redirect('admin_home')



@login_required(login_url=login_page)
@allowed_users(allowed_roles=['admin'])
def salon_details(request,id):
    salon = Salon.objects.get(id=id)
    context={'salon':salon}
    return render(request,'pages/salon.html',context)







@login_required(login_url=login_page)
@allowed_users(allowed_roles=['customer'])
def new_order(request,id):
    service = Service.objects.get(id=id)
    salon_name = service.salon.shop_name
    salon = Salon.objects.get(shop_name = salon_name)
    cart = Cart.objects.get(user=request.user)
    form = new_order_form(initial = {'service':service,'salon':salon,'cart':cart,'total':service.price})

    if request.method == 'POST':
        form = new_order_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cart')
        

    context = {'form':form}
    return render(request, 'pages/new_order.html', context)  

        

@login_required(login_url=login_page)
@allowed_users(allowed_roles=['customer'])
def order_now(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    all_cart_orders = cart.order_set.all()
    for o in all_cart_orders:
        o.order_status = "inprogress"
        o.save()
    return redirect('home')






@login_required(login_url=login_page)
@allowed_users(allowed_roles=['customer'])
def cart(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    orders = cart.order_set.all()
    all_cart_orders = orders.filter(~Q(order_status= "inprogress"))

    
    context = {'all_cart_orders':all_cart_orders,'cart':cart}
    return render(request, 'pages/cart.html', context)






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


# def new_blog(request):
#     form = new_salon_form(request.POST,request.FILES)
#     files = request.FILES.getlist('thumbnail')
#     files1 = request.FILES.getlist('title_image')
#     files2 = request.FILES.getlist('center_image')
#     if request.method == 'POST':
#         if form.is_valid():
#             obj = form.save()
#             for image in files:
#                 obj.thumbnail = image
#                 obj.save()
#             for imag in files1:
#                 obj.title_image = imag
#                 obj.save()
#             for img in files2:
#                 obj.center_image = img
#                 obj.save()        
#             return redirect('user_home')
	
#     context = {'form':form}
#     return render(request,'pages/new_salon.html',context)


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