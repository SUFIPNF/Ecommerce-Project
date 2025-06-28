from django.http import HttpResponse
from django.shortcuts import render
from products.models import Product
import random
def home(request):
    products=Product.objects.all()
    products=list(products)
    random_prod=random.sample(products,k=4)
    print(random_prod)
    context={
        'random_prod':random_prod,
    }
    return render(request,'home.html',context)

