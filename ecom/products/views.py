from django.shortcuts import render
from .models import Product,Variation
from django.core.paginator import Paginator
# Create your views here.
def store(request,category_slug=None):
    
    selected_size=request.GET.get('size')
    
    if category_slug!=None:
        products=Product.objects.filter(category__cat_slug=category_slug)
    else:
        products=Product.objects.all()
    
    if selected_size:
        products=products.filter(variation__variation_value=selected_size,variation__variation_category='size').distinct()   
        
    paginator=Paginator(products,3)
    page_number=request.GET.get("page")
    paged_products=paginator.get_page(page_number)
    per_page_prod=paged_products.object_list.count()
    counted=products.count()
        
    sizes=Variation.objects.filter(product__in=paged_products,variation_category='size',is_active=True).values_list('variation_value', flat=True).distinct()

    context={
        'products':paged_products,
        'paged_products':paged_products,
        'counted':counted,
        'prod_count': per_page_prod,
        'sizes':sizes,
        'selected_size':selected_size
    }
    return render(request,'store/store.html',context)

def product_detail(request,category_slug=None,product_slug=None):
    product=Product.objects.get(category__cat_slug=category_slug,product_slug=product_slug)
    variations=Variation.objects.filter(product=product)
    context={
        'single_product':product,
        'variations':variations
    }
    return render(request,'store/product_detail.html',context)