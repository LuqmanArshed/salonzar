from django.db import models




class Customer(models.Model):
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name


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


class Service(models.Model):
    salon = models.ForeignKey(Salon,null=True,blank=True,on_delete=models.CASCADE)
    service_name = models.CharField(max_length=200,null=True)
    price = models.IntegerField(null=True)
    def __str__(self):
        return self.service_name


class Order(models.Model):
    salon = models.ForeignKey(Salon,null=True,blank=True,on_delete=models.CASCADE)
    service = models.ForeignKey(Service,null=True,blank=True,on_delete=models.CASCADE)
    worker = models.ForeignKey(SalonWorker,null=True,blank=True,on_delete=models.CASCADE)
     
     



