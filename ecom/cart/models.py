from django.db import models
from products.models import Product,Variation
from accounts.models import Account
# Create your models here.
class Cart(models.Model):
    cart_id=models.CharField(max_length=50)
    date_added=models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.cart_id
    
    
class CartItem(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE,null=True,blank=True)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,null=True,blank=True)
    cart_item=models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    quantity=models.IntegerField()
    variations=models.ManyToManyField(Variation,null=True,blank=True)
    
    
    def sub_total(self):
        return self.cart_item.price*self.quantity
    