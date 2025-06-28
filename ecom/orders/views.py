from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from cart.models import CartItem
import random
from .models import Orders,OrderProduct,Payment
import json
from products.models import Product
from django.http import JsonResponse
# Create your views here.
@login_required(login_url='signin')
def checkout(request):
    user=request.user
    total=0
    sub_total=0
    tax=0
    grand_total=0

        
    cart_items=CartItem.objects.filter(user=request.user)
    print(cart_items)

    cart_count=0
    for cart_item in cart_items:
        total=total+(cart_item.cart_item.price*cart_item.quantity)
        cart_count+=cart_item.quantity
        
    tax=(total*8)/100
    
    grand_total=total+tax

    if request.method == 'POST':
        fname=request.POST['fname']
        print(fname)
        lname=request.POST['lname']
        print(lname)
        phone=request.POST['phone']
        print(phone)
        email=request.POST['email']
        print(email)
        add_line_1=request.POST['add_line_1']
        print(add_line_1)
        add_line_2=request.POST['add_line_2']
        print(add_line_2)
        city=request.POST['city']
        print(city)
        state=request.POST['state']
        print(state)
        country=request.POST['country']
        print(country)
        order_note=request.POST['order_note']
        print(order_note)
        order_number=random.randint(10000,99999)
        print(order_number)
        ip=request.META.get('REMOTE_ADDR')
        Orders(user=user,first_name=fname,last_name=lname,phone=phone,ip=ip,email=email,address_line_1=add_line_1,address_line_2=add_line_2,city=city,state=state,country=country,order_note=order_note,order_number=order_number,order_total=grand_total,tax=tax).save()  
        order=Orders.objects.get(user=request.user,order_number=order_number)
        print(f"ye hai hamara order:{order}")
        
        context={
            'order':order,
            'total':total,
            'tax':tax,
            'grand_total':grand_total,
            'cart_items':cart_items
        }
    
        return render(request,'orders/payments.html',context)
      
    else:
        context={
          
            'cart_count':cart_count,
            'tax':tax,
            'grand_total':grand_total,
            'cart_items':cart_items
        }
        return render(request,'orders/checkout.html',context)




def payments(request):
    body=json.loads(request.body)
    print(f'aamchi body:{body}')
    order=Orders.objects.get(user=request.user,is_ordered=False,order_number=body['orderID'])
    print(order)
    payment=Payment(user=request.user,payment_id=body['transID'],payment_method=body['payment_method'],amount_paid=order.order_total,
            status=body['status'])
    print(payment)
    payment.save()
    order.payment=payment
    order.is_ordered=True
    order.save()
    
    cart_items=CartItem.objects.filter(user=request.user)
    print(f'cartwala items:{cart_items}')
    for item in cart_items:
        print(f'dekho:{item}')
        op=OrderProduct()
        op.order=order
        print(f"mera object print ho rha hai:{op}")
        print(f'ye sab order product hai {order.id}')
        op.payment=payment
        print(payment)
        op.user=request.user
        print(request.user)
        op.product=item.cart_item
        print(item.cart_item)
        op.quantity=item.quantity
        print(item.quantity)
        op.price=item.cart_item.price
        print(item.cart_item.price)
        op.is_ordered=True
        op.save()
        cart_item=CartItem.objects.get(id=item.id)
        prod_variation=cart_item.variations.all()
        op=OrderProduct.objects.get(id=op.id)
        op.variation.set(prod_variation)
        op.save()
        product= Product.objects.get(id=item.cart_item.id)
        product.stock-=item.quantity
        product.save()
        
    CartItem.objects.filter(user=request.user).delete()
    print(f'dekho payment ka id le rha hai kya:{payment.payment_id}')
    
    data={
        'order_number':order.order_number,
        'transID':payment.payment_id,
    }
    return JsonResponse(data)
    
    # return render(request,'orders/payments.html')
    
def order_complete(request):
    order_number=request.GET.get('order_number')
    print(f'order wala number:{order_number}')
    transID=request.GET.get('payment_id')
    print(f'ye hai trans ka id:{transID}')
    try:
        order=Orders.objects.get(order_number=order_number,is_ordered=True)
        print(f'order is:{order}')
        ordered_products=OrderProduct.objects.filter(order=order.id)
        print(f'order ka product is:{ordered_products}')
        subtotal=0
        for i in ordered_products:
            subtotal=subtotal+i.product.price*i.quantity
        payment=Payment.objects.get(payment_id=transID)
        print(f'ye hai payment info:{payment}')
        context={
            'order':order,
            'op':ordered_products,
            'o_n':order_number,
            'transid':payment.payment_id,
            'payment':payment,
            'subtotal':subtotal,
        }
    except Exception:
        return redirect('home')
    return render(request,'orders/order_complete.html',context)