from django.db import models




class Customer(models.Model):
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.name


class Salon(models.Model):

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





class BusinessRegister(models.Model):
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
    no_of_workers = models.IntegerField()
    serivice_type = models.CharField(max_length=100,null=True,choices=service_category)
    address = models.TextField()
    status = models.CharField(max_length=100,null=True,choices=status_choices)
    def __str__(self):
        return self.shop_name