from django.shortcuts import render,redirect
from products.models import Product,Variation
# Create your views here.
from cart.models import Cart,CartItem
def _cart_id(request):
    cart=request.session.session_key#this will give session id
    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request,product_id):
    product_variation=[]
    product=Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        if request.method == "POST":
            for item in request.POST:   
                key=item
                value=request.POST[key]
                try:
                    variations=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                    print(f'current variation is:{variations}')
                    product_variation.append(variations)
                    print(f'Our current variation list is:{product_variation}')             
                except Exception:
                    print("koi nahi")       
     
        is_cart_item_exists=CartItem.objects.filter(cart_item=product,user=request.user).exists()
        if is_cart_item_exists:
            cart_item=CartItem.objects.filter(cart_item=product,user=request.user)
            print(f'efgh :  {cart_item}')
            ex_var_list=[]
            id=[]
            for item in cart_item:
                existing_variation=item.variations.all()
                print(existing_variation)
                ex_var_list.append(list(existing_variation)) 
                id.append(item.id)
                print(id)
            print(f'abcd : {ex_var_list}')    
            if product_variation in ex_var_list: #abhi dal rhe variations agar purani list me exist karte hai to
                index=ex_var_list.index(product_variation)
                item_id=id[index]
                item=CartItem.objects.get(cart_item=product,id=item_id)
                item.quantity+=1
                item.save()
            else:
                item=CartItem.objects.create(cart_item=product,quantity=1,user=request.user)
                if len(product_variation)>0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            item=CartItem.objects.create(cart_item=product,quantity=1,user=request.user)
            if len(product_variation)>0:
                item.variations.clear()
                item.variations.add(*product_variation)
            item.save()
            
    else:
        if request.method == "POST":
            for item in request.POST:
                key=item
                value=request.POST[key]
                try:
                    variations=Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                    product_variation.append(variations)         
                except Exception:
                    print("koi nahi")       
        try:
            cart=Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart=Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
        is_cart_item_exists=CartItem.objects.filter(cart_item=product,cart=cart).exists()
        if is_cart_item_exists:
            cart_item=CartItem.objects.filter(cart_item=product,cart=cart)
            print(f'efgh :  {cart_item}')
            ex_var_list=[]
            id=[]
            for item in cart_item:
                existing_variation=item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)  
            if product_variation in ex_var_list: #abhi dal rhe variations agar purani list me exist karte hai to
                index=ex_var_list.index(product_variation)
                item_id=id[index]
                item=CartItem.objects.get(cart_item=product,id=item_id)
                item.quantity+=1
                item.save()
            else:
                item=CartItem.objects.create(cart_item=product,quantity=1,cart=cart)
                if len(product_variation)>0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            item=CartItem.objects.create(cart_item=product,quantity=1,cart=cart)
            if len(product_variation)>0:
                item.variations.clear()
                item.variations.add(*product_variation)
            item.save()

    return redirect('cart')
    
    
def cart(request):
    if request.user.is_authenticated:
        
        cart_items=CartItem.objects.filter(user=request.user)
    else:
        try:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart)
        except Cart.DoesNotExist:
            cart_items=[]

    total=0
    tax=0
    grand_total=0
    for cart_item in cart_items:
        total=total+(cart_item.cart_item.price*cart_item.quantity)
    tax=(total*8)/100
    grand_total=total+tax
    context={

        'total':total,
        'tax':tax,
        'grand_total':grand_total,
        'cart_items':cart_items
    }
        
    return render(request,'store/cart.html',context)

def remove_cart(request,product_id,cart_item_id):
    product=Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        cart_item=CartItem.objects.get(cart_item=product,user=request.user,id=cart_item_id)
    else:
        cart_item=CartItem.objects.get(cart_item=product,id=cart_item_id)

    if cart_item.quantity>1:
        cart_item.quantity-=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def remove_cart_item(request,product_id,cart_item_id):
    product=Product.objects.get(id=product_id)
    if request.user.is_authenticated:
      
        cart_item=CartItem.objects.get(cart_item=product,user=request.user,id=cart_item_id)
    else:        
        
        cart=Cart.objects.get(cart_id=_cart_id(request))
        print(cart)
        cart_item=CartItem.objects.get(cart_item=product,id=cart_item_id)
    cart_item.delete()
    return redirect('cart')
    
    
        
        