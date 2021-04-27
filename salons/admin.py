from django.contrib import admin

# Register your models here.

from .models import Salon,Page,SalonWorker,Service

admin.site.register(Salon)
admin.site.register(Page)
admin.site.register(SalonWorker)
admin.site.register(Service)
