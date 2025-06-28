from django.db import models
from accounts.models import Account
from products.models import Product,Variation
# Create your models here.

class Payment(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    payment_id=models.CharField(max_length=50,unique=True)
    payment_method=models.CharField(max_length=50)
    amount_paid=models.FloatField()
    status=models.CharField(max_length=50)
  
    
    def __str__(self):
        return self.payment_id
status=(
    ("new","new"),
    ("accepted","accepted"),
    ("completed","completed"),
    ("cancelled","cancelled"),
)
class Orders(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    payment=models.ForeignKey(Payment,on_delete=models.CASCADE,null=True,blank=True)
    order_number=models.CharField(max_length=50)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    address_line_1=models.CharField(max_length=255)
    address_line_2=models.CharField(max_length=255,blank=True)
    country=models.CharField(max_length=50)
    state=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    order_note=models.TextField(max_length=255,blank=True)
    order_total=models.FloatField()
    tax=models.FloatField()
    status=models.CharField(max_length=10,choices=status,default="New")
    ip=models.CharField(max_length=20,blank=True)
    is_ordered=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    
    def full_address(self):
        return self.address_line_1+self.address_line_2
    def __str__(self):
        return self.order_number
    
class OrderProduct(models.Model):
    order=models.ForeignKey(Orders,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    payment=models.ForeignKey(Payment,on_delete=models.CASCADE,null=True,blank=True)
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    variation=models.ManyToManyField(Variation,blank=True)
    quantity=models.IntegerField()
    price=models.FloatField()
    is_ordered=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

