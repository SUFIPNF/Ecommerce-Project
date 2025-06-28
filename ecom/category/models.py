from django.db import models
from django.urls import reverse#reverse module use hota hai slug ko filter me working ke liye
#Create your models here.
class Category(models.Model):
    cat_name=models.CharField(max_length=50,null=True,blank=True)
    cat_slug=models.SlugField(max_length=50,null=True,blank=True)
    description=models.TextField(max_length=255,null=True,blank=True)
    cat_image=models.ImageField(upload_to="photos/categories",null=True,blank=True)
    
    def __str__(self):
        return self.cat_name
    
    def get_url(self):
        return reverse("products_by_category",args=[self.cat_slug])