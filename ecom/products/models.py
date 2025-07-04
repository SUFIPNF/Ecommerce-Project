from django.db import models
from category.models import Category
from django.urls import reverse
#Create your models here.
class Product(models.Model):
    
    name=models.CharField(max_length=50)
    product_slug=models.SlugField(null=True,blank=True)
    stock=models.IntegerField()
    price=models.FloatField()
    desc=models.TextField(max_length=255,null=True,blank=True)
    created_date=models.DateField(auto_now_add=True)
    modified_date=models.DateField(auto_now=True)
    image=models.ImageField(upload_to='photos/products')
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)
    
    def get_urls(self):
        return reverse('product_detail',args=[self.category.cat_slug,self.product_slug])
    def __str__(self):
        return self.name

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category="color",is_active=True)
    def sizes(self):
        return super(VariationManager,self).filter(variation_category="size",is_active=True)
    
    
variation_category_choice=(
    ('color','color'),
    ('size','size')
)
class Variation(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    variation_category=models.CharField(max_length=50,choices=variation_category_choice)
    variation_value=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    create_date=models.DateField(auto_now_add=True)
    objects=VariationManager()
    
    
    def __str__(self):
        return self.variation_value