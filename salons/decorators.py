from django.http import HttpResponse
from django.shortcuts import render,redirect

from .urls import *



def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('home')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request,*args,**kwargs):

			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name
			if group in allowed_roles:
				return view_func(request,*args,**kwargs)
			else:
				return HttpResponse('You are not allowed to view this page')
		return wrapper_func
	return decorator		



def admin_only(view_func):
	def wrapper_function(request,*args,**kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name
		if group == 'admin':
			return redirect('admin_home')
		if group == 'salon manager':
			return redirect('salon_user')
		if group == 'expert':
			return redirect('expert_home')						
		if group == 'customer':
			return view_func(request,*args,**kwargs)

	return wrapper_function		