from django.db import models

# Create your models here.
class Department(models.Model):
    Dep_name = models.CharField(max_length=70)
    Dep_desc = models.CharField(max_length=100)
    Dep_head = models.CharField(max_length=70)

    def __str__(self):
        return super().__str__() 
    
class Employee(models.Model):
    Name = models.CharField(max_length=50)
    Email = models.EmailField()
    Contact=models.IntegerField()
    Image=models.ImageField(upload_to='image')
    Code=models.CharField(max_length=20)
    Dept=models.CharField(max_length=40,null=True)    

class Query(models.Model):
    Name = models.CharField(max_length=50)
    Email = models.EmailField()
    Dept=models.CharField(max_length=40)    
    Query= models.TextField()
    Status = models.CharField(default="pending")
    Reply = models.CharField(null=True)

class Item(models.Model):
    Item_name = models.CharField(max_length=50)
    Item_desc = models.TextField()
    Item_price = models.IntegerField()
    Item_image = models.ImageField(upload_to='image')
    Item_color = models.CharField(max_length=50)
    Item_category = models.CharField(max_length=50)
    Item_quantity = models.IntegerField(null=True)

class Order(models.Model):
    order_id =  models.CharField(max_length=100)
    amount = models.IntegerField()
    razorpay_id = models.CharField(max_length=100,blank=True)  
    payment_status = models.BooleanField(default=False)

