from django.contrib import admin

# Register your models here.

from .models import Salon,BusinessRegister

admin.site.register(Salon)
admin.site.register(BusinessRegister)