from django.forms import ModelForm

from django.contrib.auth.forms import UserCreationForm


from django.contrib.auth.models import User
from django import forms

from .models import Order, Page, Product, ProductOrder, Query,Salon,SalonWorker,Service, Slot
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Field
from crispy_forms.bootstrap import AppendedText, PrependedText

from django.forms import ClearableFileInput



class new_salon_form(ModelForm):
	class Meta:
		model = Page
		fields = '__all__'


class salon_worker_form(ModelForm):
	class Meta:
		model = SalonWorker
		fields = '__all__'


class new_order_form(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(new_order_form, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.form_show_labels = False
		self.fields['slot'].required = True
		self.fields['total'].widget.attrs['readonly'] = True
		self.fields['service'].widget.attrs['readonly'] = True


	def getslots(self,id):
		salon = Salon.objects.get(id=id)
		self.fields['slot'].queryset = Slot.objects.filter(salon=salon)


	class Meta:
		model = Order
		fields = ['cart','salon','service','type','slot','order_date','order_status','total']
		widgets = {'cart':forms.HiddenInput(),'salon':forms.HiddenInput(),
		'order_date':forms.HiddenInput(),'order_status':forms.HiddenInput(),'order_time':forms.HiddenInput()}



class assign_worker_order(ModelForm):

	def getworkers(self,id):
		salon = Salon.objects.get(id=id)
		self.fields['worker'].queryset = SalonWorker.objects.filter(salon=salon)
	class Meta:
		model = Order
		fields = ['worker']




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
		

class edit_slot_form(ModelForm):
	class Meta:
		model = Slot
		fields = ['slot_start_time','slot_end_time']
		

class busines_resgiter_form(ModelForm):
	def __init__(self, *args, **kwargs):
		super(busines_resgiter_form, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.form_show_labels = False
		
	class Meta:
		model = Salon
		fields = ['shop_name','phone','email','no_of_workers','serivice_type','address','status']
		


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']




class product_form(ModelForm):
	class Meta:
		model = Product
		fields = ['salon','product_name','product_price','product_stock','discount']


class product_order_form(ModelForm):
	def __init__(self, *args, **kwargs):
		super(product_order_form, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.form_show_labels = False
		self.fields['product'].widget.attrs['readonly'] = True

	class Meta:
		model = ProductOrder
		fields = ['cart','salon','product','quantity','type','order_date','order_status','order_time']
		widgets = {'status': forms.HiddenInput(),'cart':forms.HiddenInput(),'salon':forms.HiddenInput(),
		'order_date':forms.HiddenInput(),'order_status':forms.HiddenInput(),'order_time':forms.HiddenInput()}



class change_prduct_quantity(ModelForm):
	def __init__(self, *args, **kwargs):
		super(change_prduct_quantity, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.form_show_labels = False

	class Meta:
		model = ProductOrder
		fields = ['quantity']
