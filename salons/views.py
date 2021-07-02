from .models import *
from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users,admin_only
from django.db.models import Q
import datetime
import time




def logoutuser(request):
	logout(request)
	return redirect('login_page')

@unauthenticated_user
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
            return redirect('login_page')
        

    context = {'form':form}
    return render(request, 'pages/register.html', context)


def business_registerPage(request):
    form = busines_resgiter_form(initial={'status':'Pending'})
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
    return render(request, 'pages/service_register_page.html', context)    



def temp(request):
    all_salons = Salon.objects.filter(status='approved')
    context={'all_salons':all_salons}
    return render(request,'pages/temp.html',context)


@admin_only
def home(request):
    all_salons = Salon.objects.filter(status='approved')
    all_products = Product.objects.all()
    context={'all_salons':all_salons,'all_products':all_products}
    return render(request,'pages/home.html',context)



@login_required(login_url=login_page)
@allowed_users(allowed_roles=['salon manager'])
def salon_user_page(request):
    user = request.user
    print(user)
    salon = Salon.objects.get(user=user)
    approvals = Order.objects.filter(salon=salon,order_status='pending')
    total_approvals= Order.objects.filter(salon=salon,order_status='pending').count()
    appointments = Order.objects.filter(salon=salon,order_status='inprogress')
    p_orders = ProductOrder.objects.filter(salon=salon,order_status='inprogress')
    total_p_orders = ProductOrder.objects.filter(salon=salon,order_status='inprogress').count()
    completed = Order.objects.filter(salon=salon,order_status='complete')
    all_workers = SalonWorker.objects.filter(salon=salon)
    all_products = Product.objects.filter(salon=salon)
    all_services = Service.objects.filter(salon=salon)
    all_slots = Slot.objects.filter(salon=salon)
    context={'p_orders':p_orders,'approvals':approvals,'all_slots':all_slots,'salon':salon,'all_workers':all_workers,
    'appointments':appointments,'completed':completed,'all_products':all_products,
    'all_services':all_services,'total_approvals':total_approvals,'total_p_orders':total_p_orders}
    return render(request,'pages/salon_user.html',context)



@login_required(login_url=login_page)
@allowed_users(allowed_roles=['salon manager'])
def salon_user_setting(request):
    user = request.user
    print(user)
    salon = Salon.objects.get(user=user)
    approvals = Order.objects.filter(salon=salon,order_status='pending')
    appointments = Order.objects.filter(salon=salon,order_status='inprogress')
    completed = Order.objects.filter(salon=salon,order_status='complete')
    all_workers = SalonWorker.objects.filter(salon=salon)
    all_products = Product.objects.filter(salon=salon)
    all_services = Service.objects.filter(salon=salon)
    all_slots = Slot.objects.filter(salon=salon)
    pc_orders = ProductOrder.objects.filter(salon=salon,order_status='complete')
    context={'pc_orders':pc_orders,'approvals':approvals,'all_slots':all_slots,'salon':salon,'all_workers':all_workers,'appointments':appointments,'completed':completed,'all_products':all_products,'all_services':all_services}
    return render(request,'pages/salonuser_settings.html',context)








@login_required(login_url=login_page)
@allowed_users(allowed_roles=['salon manager'])
def change_order_status(request,id):
    order = Order.objects.get(id=id)
    order.order_status = 'complete'
    order.save()
    return redirect('salon_user')



@login_required(login_url=login_page)
@allowed_users(allowed_roles=['salon manager'])
def product_order_status(request,id):
    order = ProductOrder.objects.get(id=id)
    product = Product.objects.get(id=order.product.id)
    product.product_stock = product.product_stock - order.quantity
    product.save()
    order.order_status = 'complete'
    order.save()
    return redirect('salon_user')



@login_required(login_url=login_page)
@allowed_users(allowed_roles=['salon manager'])
def add_worker(request,id):
    salon = Salon.objects.get(id=id)
    form = salon_worker_form(initial = {'salon':salon})
    if request.method == 'POST':
        form = salon_worker_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('salon_user')
        

    context = {'form':form}
    return render(request, 'pages/new_worker.html', context)



@login_required(login_url=login_page)
@allowed_users(allowed_roles=['salon manager'])
def edit_worker(request,id):
    worker = SalonWorker.objects.get(id=id)
    form = salon_worker_form(instance=worker)
    if request.method == 'POST':
        form = salon_worker_form(request.POST,instance=worker)
        if form.is_valid():
            form.save()
            return redirect('salon_user')
        

    context = {'form':form}
    return render(request, 'pages/new_worker.html', context)






@login_required(login_url=login_page)
@allowed_users(allowed_roles=['salon manager'])
def add_service(request,id):
    salon = Salon.objects.get(id=id)
    form = salon_serice_form(initial = {'salon':salon})
    if request.method == 'POST':
        form = salon_serice_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('salon_user')
        

    context = {'form':form}
    return render(request, 'pages/new_service.html', context)


@login_required(login_url=login_page)
@allowed_users(allowed_roles=['salon manager'])
def edit_service(request,id):
    service = Service.objects.get(id=id)
    form = salon_serice_form(instance=service)
    if request.method == 'POST':
        form = salon_serice_form(request.POST,instance=service)
        if form.is_valid():
            form.save()
            return redirect('salon_user')
        

    context = {'form':form}
    return render(request, 'pages/new_service.html', context)    

@login_required(login_url=login_page)
@allowed_users(allowed_roles=['salon manager'])
def add_slot(request,id):
    salon = Salon.objects.get(id=id)
    form = slot_form(initial = {'salon':salon})
    if request.method == 'POST':
        form = slot_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('salon_user')
        

    context = {'form':form}
    return render(request, 'pages/new_slot.html', context)

@login_required(login_url=login_page)
@allowed_users(allowed_roles=['salon manager'])
def edit_slot(request,id):
    slot = Slot.objects.get(id=id)
    form = edit_slot_form(instance=slot)
    if request.method == 'POST':
        form = edit_slot_form(request.POST,instance=slot)
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
def edit_product(request,id):
    product = Product.objects.get(id=id)
    form = product_form(instance=product)
    if request.method == 'POST':
        form = product_form(request.POST,request.FILES,instance=product)
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
def assign_worker(request,id):
    order = Order.objects.get(id=id)
    form = assign_worker_order(request.POST,instance=order)
    form.getworkers(order.salon.id)
    if request.method == 'POST':
        if form.is_valid():
            obj=form.save()
            obj.order_status = 'inprogress'
            obj.save()
            return redirect('salon_user')
        

    context = {'form':form}
    return render(request, 'pages/assign_worker.html', context)



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


@login_required(login_url=login_page)
@allowed_users(allowed_roles=['salon manager'])
def cancel_order(request,id):
    order = Order.objects.get(id=id)
    order.order_status = 'reject'
    order.save()
    return redirect('salon_user')



def register_option(request):
    context={}
    return render(request,'pages/register_option.html',context)






@login_required(login_url=login_page)
@allowed_users(allowed_roles=['admin'])
def admin_home(request):
    all_requests = Salon.objects.filter(status='pending')
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
    if service.discount != 0:
        total_discount = (service.price * service.discount)/100
        discounted =  service.price - total_discount
    else:
        discounted =  service.price 

    salon_name = service.salon.shop_name
    salon = Salon.objects.get(shop_name = salon_name)
    cart = Cart.objects.get(user=request.user)
    date = datetime.date.today()
    time = datetime.datetime.now().time()
    form = new_order_form(initial = {'service':service,'salon':salon,'cart':cart,'total':discounted,'order_date':date,'order_status':'cartpending'})
    form.getslots(salon.id)
    if request.method == 'POST':
        form = new_order_form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Service has been added to cart ')
            return redirect('salon_page',salon.id)
        

    context = {'form':form}
    return render(request, 'pages/new_order.html', context)  

        

@login_required(login_url=login_page)
@allowed_users(allowed_roles=['customer'])
def new_product_order(request,id):
    product = Product.objects.get(id=id)
    total_discount = (product.product_price * product.discount)/100
    discounted =  product.product_price - total_discount


    salon_name = product.salon.shop_name
    salon = Salon.objects.get(shop_name = salon_name)
    if product.product_stock == 0:
        messages.warning(request,'Product is not in-stock')
        return redirect('salon_page',salon.id)

    cart = Cart.objects.get(user=request.user)
    date = datetime.date.today()
    time = datetime.datetime.now().time()
    form = product_order_form(initial = {'product':product,'salon':salon,'cart':cart,'order_date':date,'order_status':'pending'})
    if request.method == 'POST':
        form = product_order_form(request.POST)
        if form.is_valid():
            obj=form.save()
            quantities = form.cleaned_data['quantity']
            if discounted != 0:
                obj.total = discounted * quantities
                obj.save()
            else:
                obj.total = product.product_price * quantities
                obj.save()  

            messages.success(request,'Product has been added to cart ')
            return redirect('salon_page',salon.id)
        

    context = {'form':form}
    return render(request, 'pages/product_order.html', context) 









@login_required(login_url=login_page)
@allowed_users(allowed_roles=['customer'])
def order_now(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    time = datetime.datetime.now()
    all_cart_orders = cart.order_set.all()
    all_product_orders = cart.productorder_set.all()
    for o in all_cart_orders:
        o.order_status = "pending"
        o.order_time = time
        o.save()

    for p in all_product_orders:
        p.order_status = "inprogress"
        p.order_time = time
        p.save()    
    return redirect('home')








@login_required(login_url=login_page)
@allowed_users(allowed_roles=['customer'])
def cart(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    orders = cart.order_set.all()
    product_orders = cart.productorder_set.all()
    all_cart_orders = orders.filter(order_status= "cartpending")
    all_product_orders = product_orders.filter(~Q(order_status= "inprogress"))

    
    context = {'all_cart_orders':all_cart_orders,'cart':cart,'all_product_orders':all_product_orders}
    return render(request, 'pages/cart.html', context)


@login_required(login_url=login_page)
@allowed_users(allowed_roles=['customer'])
def all_appointments(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    orders = cart.order_set.all()
    appointments = orders.filter(order_status= "inprogress")
    c_appointments = orders.filter(order_status= "reject")
    
    context = {'appointments':appointments,'cart':cart,'c_appointments':c_appointments}
    return render(request, 'pages/appointments.html', context)




@login_required(login_url=login_page)
@allowed_users(allowed_roles=['customer'])
def all_queries(request):
    user = request.user
    queries = Query.objects.filter(user=user)
    open_queries = queries.filter(status= "open")
    close_queries = queries.filter(status= "close")
    
    context = {'queries':queries,'open_queries':open_queries,'close_queries':close_queries}
    return render(request, 'pages/all_customer_queries.html', context)


@login_required(login_url=login_page)
@allowed_users(allowed_roles=['customer'])
def ask_question(request):
    user = request.user
    form = question_form(initial = {'user':user,'status':'open'})
    if request.method == 'POST':
        form = question_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('query_page')
        

    context = {'form':form}
    return render(request, 'pages/question_query.html', context)



@login_required(login_url=login_page)
@allowed_users(allowed_roles=['expert'])
def answer_query(request,id):
    query = Query.objects.get(id=id)
    form = answer_form(instance=query)
    if request.method == 'POST':
        form = answer_form(request.POST,instance=query)
        if form.is_valid():
            obj=form.save()
            obj.status = 'close'
            obj.save()
            return redirect('expert_home')
        

    context = {'form':form,'query':query}
    return render(request, 'pages/answer_page.html', context)







@login_required(login_url=login_page)
@allowed_users(allowed_roles=['expert'])
def expert_home(request):
    all_queries = Query.objects.filter(status='open')   
    context = {'all_queries':all_queries}
    return render(request, 'pages/expert_home.html', context)





@login_required(login_url=login_page)
@allowed_users(allowed_roles=['customer'])
def removefromcart(request,id):
    order = ProductOrder.objects.get(id=id)
    order.delete()
    return redirect('cart')




@login_required(login_url=login_page)
@allowed_users(allowed_roles=['customer'])
def changeorderquantity(request,id):
    order = ProductOrder.objects.get(id=id)
    product = Product.objects.get(id=order.product.id)
    form = change_prduct_quantity(instance=order)
    if request.method == 'POST':
        form = change_prduct_quantity(request.POST,instance=order)
        if form.is_valid():
            obj=form.save()
            quantities = form.cleaned_data['quantity']
            obj.total = product.product_price * quantities
            obj.save()
            messages.success(request,'Product has been updated ')
            return redirect('cart')
        

    context = {'form':form}
    return render(request, 'pages/chnageq.html', context)




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