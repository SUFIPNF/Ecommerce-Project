from .models import Cart,CartItem
from .views import _cart_id
def cart_count(request):
    if 'admin' in request.path:
        return {}
    else:
        try:
            if request.user.is_authenticated:
                cart_items=CartItem.objects.filter(user=request.user)
            else:
                cart=Cart.objects.get(cart_id=_cart_id(request))
                cart_items=CartItem.objects.filter(cart=cart)
                
            count=0
            for cart_item in cart_items:
                count=count+cart_item.quantity
                print(f'count: {cart_items}')
        except Exception:
            count=0
    return dict(count=count)