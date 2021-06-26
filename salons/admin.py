from django.contrib import admin

# Register your models here.

from .models import Cart, Order, Product, ProductOrder, Query, Salon,Page,SalonWorker,Service, Slot

admin.site.register(Salon)
admin.site.register(Page)
admin.site.register(SalonWorker)
admin.site.register(Service)
admin.site.register(Cart)
admin.site.register(Slot)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Query)
admin.site.register(ProductOrder)


