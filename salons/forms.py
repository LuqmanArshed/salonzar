from django.forms import ModelForm

from django.contrib.auth.forms import UserCreationForm


from django.contrib.auth.models import User
from django import forms

from .models import Order, Page, Product, Query,Salon,SalonWorker,Service, Slot


class new_salon_form(ModelForm):
	class Meta:
		model = Page
		fields = '__all__'


class salon_worker_form(ModelForm):
	class Meta:
		model = SalonWorker
		fields = '__all__'


class new_order_form(ModelForm):
	class Meta:
		model = Order
		fields = '__all__'


class question_form(ModelForm):
	class Meta:
		model = Query
		fields = ['user','title','question','status']


class answer_form(ModelForm):
	class Meta:
		model = Query
		fields = ['answer']


class salon_serice_form(ModelForm):
	class Meta:
		model = Service
		fields = '__all__'


class slot_form(ModelForm):
	class Meta:
		model = Slot
		fields = '__all__'


class busines_resgiter_form(ModelForm):
	class Meta:
		model = Salon
		fields = ['shop_name','phone','email','no_of_workers','serivice_type','address','status']
		widgets = {'status': forms.HiddenInput()}


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']




class product_form(ModelForm):
	class Meta:
		model = Product
		fields = ['salon','product_name','product_price']