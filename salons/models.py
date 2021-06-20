from django.db import models


from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE




class Page(models.Model):

    JOHAR = 'johar town'
    PIA = 'pia Society'
    DHA = 'dha'
    BHARIA = 'bahria town'
    

    category_choices = [

        (JOHAR,'johar town'),
        (PIA,'pia Society'),
        (DHA,'dha'),
        (BHARIA,'bahria town')
    ]
    title = models.CharField(max_length=100,null=True,blank=True)
    header = models.TextField(null=True,blank=True)
    location = models.CharField(max_length=50,null=True,blank=True,choices=category_choices)
    details = models.TextField(null=True,blank=True)
    thumbnail = models.ImageField(upload_to='SalomImages/',null=True,blank=True)
    title_image = models.ImageField(upload_to='SalonImages/',null=True,blank=True)
    center_image = models.ImageField(upload_to='SalonImages/',null=True,blank=True) 
    def __str__(self):
        return str(self.title)





class Salon(models.Model):
    HOME = 'home service'
    SHOP = 'shop'
    BOTH = 'both'
    PENDING ='pending'
    APPROVED = 'approved'
    service_category =[
        (HOME,'Home Service'),
        (SHOP,'Shop'),
        (BOTH,'Both')

    ]
    status_choices =[
        (PENDING,'Pending'),
        (APPROVED,'Approved')

    ]
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    no_of_workers = models.IntegerField(null=True)
    serivice_type = models.CharField(max_length=100,null=True,choices=service_category)
    address = models.TextField(null=True)
    status = models.CharField(max_length=100,null=True,choices=status_choices)
    thumbnail = models.ImageField(upload_to='SalonImages/',null=True,blank=True)    
    def __str__(self):
        return self.shop_name

   

class SalonWorker(models.Model):
    BUSY = 'busy'
    AVAILABLE = 'available'
    worker_choices =[
        (BUSY,'busy'),
        (AVAILABLE,'available'),
    ]
    salon = models.ForeignKey(Salon,null=True,blank=True,on_delete=models.CASCADE)
    worker_name = models.CharField(max_length=200,null=True)
    worker_contact = models.IntegerField(null=True)
    worker_status = models.CharField(max_length=200,null=True,choices=worker_choices)
    def __str__(self):
        return self.worker_name


class Slot(models.Model):
    BOOKED = 'booked'
    AVAILABLE = 'available'
    slot_choices = [
        (BOOKED,'booked'),
        (AVAILABLE,'available')
    ]
    salon = models.ForeignKey(Salon,null=True,blank=True,on_delete=models.CASCADE)
    slot_start_time = models.CharField(max_length=200,null=True)
    slot_end_time = models.CharField(max_length=200,null=True)
    slot_status = models.CharField(max_length=200,null=True,choices=slot_choices)
    def __str__(self):
        return self.slot_start_time + " to " + self.slot_end_time







class Service(models.Model):
    salon = models.ForeignKey(Salon,null=True,blank=True,on_delete=models.CASCADE)
    service_name = models.CharField(max_length=200,null=True)
    price = models.IntegerField(null=True)
    def __str__(self):
        return self.service_name



class Cart(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    address = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=200,null=True)



class Order(models.Model):
    INPROGRESS = 'inprogress'
    PENDING = 'pending'
    COMPLETE = 'complete'
    SHOP = 'shop'
    HOME = 'home'
    order_choices = [
        (INPROGRESS,'inprogress'),
        (PENDING,'pending'),
        (COMPLETE,'complete')
    ]
    type_choices = [
        (SHOP,'shop'),
        (HOME,'home')
    ]
    cart = models.ForeignKey(Cart,null=True,blank=True,on_delete=models.CASCADE)
    salon = models.ForeignKey(Salon,null=True,blank=True,on_delete=models.CASCADE)
    service = models.ForeignKey(Service,null=True,blank=True,on_delete=models.CASCADE)
    worker = models.ForeignKey(SalonWorker,null=True,blank=True,on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot,null=True,blank=True,on_delete=models.CASCADE)
    type = models.CharField(max_length=200,null=True,blank=True,choices=type_choices)
    order_date = models.DateField(null=True,blank=True)
    order_status = models.CharField(max_length=200,null=True,blank=True,choices=order_choices)
    total = models.IntegerField(null=True,blank=True)



     
     
class Product(models.Model):
    salon = models.ForeignKey(Salon,null=True,blank=True,on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200,null=True,blank=True)
    product_price = models.IntegerField(null=True,blank=True)
    product_image= models.ImageField(upload_to='Products/',null=True,blank=True)
    def __str__(self):
        return self.product_name



class Query(models.Model):
    OPEN = 'open'
    CLOSE = 'close'
    query_choices = [
        (OPEN,'open'),
        (CLOSE,'close')
    ]
    user = models.CharField(max_length=200,null=True,blank=True)
    title = models.CharField(max_length=200,null=True,blank=True)
    question = models.TextField(max_length=500,null=True,blank=True)
    answer = models.TextField(max_length=500,null=True,blank=True)
    status = models.CharField(max_length=50,choices=query_choices,null=True,blank=True)
    def __str__(self):
        return self.title
