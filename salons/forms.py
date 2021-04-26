from django.forms import ModelForm

from django.contrib.auth.forms import UserCreationForm


from django.contrib.auth.models import User
from django import forms

from .models import *


class new_salon_form(ModelForm):
	class Meta:
		model = Salon
		fields = '__all__'



class busines_resgiter_form(ModelForm):
	class Meta:
		model = BusinessRegister
		fields = ['shop_name','phone','email','no_of_workers','serivice_type','address','status']
		widgets = {'status': forms.HiddenInput()}


class CreateUserForm(UserCreationForm):
	contact = forms.CharField(max_length=32)
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2','contact']
